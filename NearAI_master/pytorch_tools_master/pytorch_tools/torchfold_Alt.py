import collections
import torch
from torch.autograd import Variable

#This is a modified version of the original torchfold.py file for me to use in
#my project. The functions that were changed are _batch_args and apply.
class Fold(object):

    class Node(object):
        def __init__(self, op, step, index, args):
            self.op = op
            self.step = step
            self.index = index
            self.args = args
            self.split_idx = -1
            self.batch = True

        def split(self, num):
            """Split resulting node, if function returns multiple values."""
            nodes = []
            for idx in range(num):
                nodes.append(Fold.Node(
                    self.op, self.step, self.index, self.args))
                nodes[-1].split_idx = idx
            return tuple(nodes)

        def nobatch(self):
            self.batch = False
            return self

        def get(self, values):
            if self.split_idx >= 0:
                return values[self.step][self.op][self.split_idx][self.index]
            else:
                return values[self.step][self.op][self.index]

        def __repr__(self):
            return "[%d:%d]%s" % (
                self.step, self.index, self.op)

    def __init__(self, volatile=False, cuda=True):
        self.steps = collections.defaultdict(
            lambda: collections.defaultdict(list))
        self.cached_nodes = collections.defaultdict(dict)
        self.total_nodes = 0
        self.volatile = volatile
        self._cuda = cuda

    def cuda(self):
        self._cuda = True
        return self

    def add(self, op, args):
        """Add op to the fold."""
        self.total_nodes += 1
        if args not in self.cached_nodes[op]:
            step = max([0] + [arg.step + 1 for arg in args
                              if isinstance(arg, Fold.Node)])
            node = Fold.Node(op, step, len(self.steps[step][op]), args)
            self.steps[step][op].append(args)
            self.cached_nodes[op][args] = node
        return self.cached_nodes[op][args]
    
    #This function has been modified from the original version.
    def _batch_args(self, dim, op, values, arg_list):
        if op == 'process_children':
            
            #In order to accomodate trees that are not binary, we use the concept
            #of continuous binary trees.
            #The weight for each child node is a linear combination of left weight
            #and right weight.
            #The closer the child is to the leftmost child, the greater the coefficient
            #in front of the left weight.
            #The closer the child is to the rightmost child, the greater the coefficient
            #in front of the right weight.
            
            #In order to keep the code clean and efficient, instead of taking the
            #linear combination of the left and right weights, I take the linear
            #combination of the inputs from the children nodes going into left weight
            #and call it left_h and left_c.
            #Similarly, I take the linear combination of the inputs from the children
            #nodes going into right weight and call it right_h and right_c.
            
            #Both ways are equivalent in the end.
            left_h = []; left_c = []; right_h = []; right_c = []; word_indices = []
            for arg in arg_list:
                m = int((len(arg)-1)/2)
                lh = []; lc = []; rh = []; rc = []
                lh.append(arg[0].get(values))
                lc.append(arg[1].get(values))
                for k in range(1, m):
                    r = 1.0*k/(m-1); l = 1-r
                    lh.append(l*arg[2*k].get(values))
                    lc.append(l*arg[2*k+1].get(values))
                    rh.append(r*arg[2*k].get(values))
                    rc.append(r*arg[2*k+1].get(values))
                left_h.append(sum(lh)); left_c.append(sum(lc))
                if len(rh) > 0:
                    right_h.append(sum(rh))
                else:
                    right_h.append(Variable(torch.cuda.FloatTensor(1, dim).zero_()))
                if len(rc) > 0:
                    right_c.append(sum(rc))
                else:
                    right_c.append(Variable(torch.cuda.FloatTensor(1, dim).zero_()))
                    
                #Add the index of the node's word at the end.
                word_indices.append(arg[-1])
            res = [torch.cat(left_h, 0),
                   torch.cat(left_c, 0),
                   torch.cat(right_h, 0),
                   torch.cat(right_c, 0),
                   Variable(torch.cuda.LongTensor(word_indices))]
        elif op == 'logits':
            
            #This is the logits case, where we are trying to get the raw outputs
            #for each tree in the batch.
            r = []
            for arg in arg_list:
                if isinstance(arg, (list, tuple)):
                    r.append(arg[0].get(values))
                else:
                    r.append(arg.get(values))
            res = [torch.cat(r, 0)]
        else:
            
            #This is the leaf node case where we just return the word index
            #as a variable.
            r = []
            for arg in arg_list:
                r.append(arg[0])
            res = [Variable(torch.cuda.LongTensor(r))]
        return res
    
    #This function has been modified from the original version.
    def apply(self, model, nodes):
        """Apply current fold to given neural module."""
        values = {}; dim = model.size
        for step in sorted(self.steps.keys()):
            values[step] = {}
            for op in self.steps[step]:
                
                #If we're dealing with logits, don't split, eitherwise we need
                #to split, one for hidden state and one for cell state.
                if op == 'logits':
                    values[step][op] = []
                    split = False
                else:
                    values[step][op] = [[], []]
                    split = True
                func = getattr(model, op)
                
                #Divide all the computations of type op at the current step
                #into chunks of size 128.
                for i in range(0, len(self.steps[step][op]), 128):
                    chunked_batch = self.steps[step][op][i:i+128]
                    try:
                        chunked_batched_args = self._batch_args(dim, op, values, chunked_batch)
                    except Exception:
                        print("Error while executing node %s[%d] with args: %s" % (
                            op, step, self.steps[step][op]))
                        raise
                    batch_res = func(*chunked_batched_args)
                    
                    #Save all of the results of type op at the current step to
                    #the values dictionary.
                    if split:
                        for i in range(2):
                            values[step][op][i] += batch_res[i].split(1)
                    else:
                        values[step][op] += batch_res.split(1)
        try:
            return self._batch_args(dim, 'logits', values, nodes)
        except Exception:
            print("Retrieving %s" % nodes)
            for lst in nodes:
                if isinstance(lst[0], Fold.Node):
                    print(', '.join([str(x.get(values).size()) for x in lst]))
            raise
