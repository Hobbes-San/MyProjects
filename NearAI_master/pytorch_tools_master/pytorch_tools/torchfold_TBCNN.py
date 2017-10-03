import collections
from itertools import zip_longest

import torch
from torch.autograd import Variable
import torch.nn as nn
from torch import optim
import torch.nn.functional as F


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

    def _batch_args(self, dim, length_list, arg_lists, values):
        res = []; k = 0; op = ''
        for arg in arg_lists:
            n = len(arg)
            if arg[0] is None or isinstance(arg[0], Fold.Node):
                if length_list[0] == 1:
                    r = []
                    for x in arg:
                        r.append(x.get(values))
                    res.append(torch.cat(r, 0))
                else:
                    op = 'process_children'
                    left_h = torch.cuda.FloatTensor(n, dim).zero_()
                    left_c = torch.cuda.FloatTensor(n, dim).zero_()
                    right_h = torch.cuda.FloatTensor(n, dim).zero_()
                    right_c = torch.cuda.FloatTensor(n, dim).zero_()
                    if k % 2 == 0:
                        for j in range(n):
                            m = (length_list[j]-1)/2
                            if m == 1:
                                r = 0; l = 1
                            else:
                                r = 1.0 * int((k-1)/2)/(m-1); l = 1-r
                            if arg[j] is not None:
                                left_h[j] += (l * arg[j].get(values).data.view(-1))
                                right_h[j] += (r * arg[j].get(values).data.view(-1))
                    else:
                        for j in range(n):
                            m = (length_list[j]-1)/2
                            if m == 1:
                                r = 0; l = 1
                            else:
                                r = 1.0 * int((k-1)/2)/(m-1); l = 1-r
                            if arg[j] is not None:
                                left_c[j] += (l * arg[j].get(values).data.view(-1))
                                right_c[j] += (r * arg[j].get(values).data.view(-1))
            else:
                try:
                    var = Variable(torch.cuda.LongTensor(arg), volatile=self.volatile)  
                    res.append(var)
                except:
                    print("Constructing LongTensor from %s" % str(arg))
                    raise
            k += 1
        if op == 'process_children':
            res += [Variable(left_h), Variable(left_c), Variable(right_h), Variable(right_c)]
        return res

    def apply(self, model, nodes):
        """Apply current fold to given neural module."""
        values = {}; dim = model.size
        for step in sorted(self.steps.keys()):
            values[step] = {}
            for op in self.steps[step]:
                if op == 'logits':
                    values[step][op] = []
                    split = False
                else:
                    values[step][op] = [[], []]
                    split = True
                func = getattr(model, op)
                for i in range(0, len(self.steps[step][op]), 128):
                    chunked_batch = self.steps[step][op][i:i+128]
                    try:
                        chunked_batched_args = self._batch_args(dim,
                                           [len(input_) for input_ in self.steps[step][op]],
                                           zip_longest(*chunked_batch), values)
                    except Exception:
                        print("Error while executing node %s[%d] with args: %s" % (
                            op, step, self.steps[step][op]))
                        raise
                    batch_res = func(*chunked_batched_args)
                    if split:
                        for i in range(2):
                            values[step][op][i] += batch_res[i].split(1)
                    else:
                        values[step][op] += batch_res.split(1)
        try:
            return self._batch_args(dim, [1], nodes, values)
        except Exception:
            print("Retrieving %s" % nodes)
            for lst in nodes:
                if isinstance(lst[0], Fold.Node):
                    print(', '.join([str(x.get(values).size()) for x in lst]))
            raise


class Unfold(object):
    """Replacement of Fold for debugging, where it does computation right away."""

    class Node(object):

        def __init__(self, tensor):
            self.tensor = tensor

        def __repr__(self):
            return str(self.tensor)

        def nobatch(self):
            return self

        def split(self, num):
            return [Unfold.Node(self.tensor[i]) for i in range(num)]

    def __init__(self, model, volatile=False, cuda=False):
        self.model = model
        self.volatile = volatile
        self._cuda = cuda

    def cuda(self):
        self._cuda = True
        return self

    def _arg(self, arg):
        if isinstance(arg, Unfold.Node):
            return arg.tensor
        elif isinstance(arg, int):
            if self._cuda:
                return Variable(torch.cuda.LongTensor([arg]), volatile=self.volatile)
            else:
                return Variable(torch.LongTensor([arg]), volatile=self.volatile)
        else:
            return arg

    def add(self, op, *args):
        values = []
        for arg in args:
            values.append(self._arg(arg))
        res = getattr(self.nn, op)(*values)
        return Unfold.Node(res)

    def apply(self, model, nodes):
        if nn != self.nn:
            raise ValueError("Expected that nn argument passed to constructor and passed to apply would match.")
        result = []
        for n in nodes:
            result.append(torch.cat([self._arg(a) for a in n]))
        return result
