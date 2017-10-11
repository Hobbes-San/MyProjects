import javalang_master.javalang
import clang_38.clang.cindex

def parse_tree_Java(code):
    tokens = javalang_master.javalang.tokenizer.tokenize(code)
    parser = javalang_master.javalang.parser.Parser(tokens)
    parse_tree = parser.parse()
    return parse_tree

def parse_tree_Cpp(code):
    source_code = code.encode('utf-8'); virtual_filename = ('virtual.hpp').encode('utf-8')
    parse_tree = clang_38.clang.cindex.TranslationUnit.from_source(filename=virtual_filename,
        unsaved_files=[(virtual_filename, source_code)])
    return parse_tree

def index_tree_Java(tree, word2idx):
    if not isinstance(tree, javalang_master.javalang.ast.Node):
        return None
    word = str(tree.__class__.__name__)
    indexed_node = Node()
    indexed_node.val = word2idx[word]
    for attr in tree.attrs:
        value = getattr(tree, attr)
        if not value:
            continue
        if isinstance(value, (list, set, tuple)):
            for x in value:
                child = index_tree_Java(x, word2idx)
                if child is not None:
                    indexed_node.children.append(child)
        else:
            child = index_tree_Java(value, word2idx)
            if child is not None:
                indexed_node.children.append(child)
    return indexed_node

def index_tree_Cpp(cu, word2idx):
    word = str(cu.kind)
    indexed_node = Node()
    indexed_node.val = word2idx[word]
    for child in cu.get_children():
        indexed_node.children.append(index_tree_Cpp(child, word2idx))
    return indexed_node

class Node:
    def __init__(self):
        self.val = None
        self.children = []
    
    def is_leaf(self):
        return (len(self.children) == 0)
    
    def traverse(self):
        yield self
        for child in self.children:
            for descendant in child.traverse():
                yield descendant

def deserialize(L, stack):
    if len(L) <= 2:
        return
    for i in range(1, len(L)-1):
        token = L[i]
        if token != ')':
            current = Node(); current.val = L[i]
            parent = stack[-1]; parent.children.append(current)
            stack.append(current)
        else:
            stack.pop()
    
def serialize(tree, result):
    result.append(str(tree.val))
    for child in tree.children:
        serialize(child, result)
    result.append(')')
    
#The main model.
class RecursiveModel(nn.Module):

    def __init__(self, vocab_size, size):
        super(RecursiveModel, self).__init__()
        self.vocab_size = vocab_size
        self.size = size
        self.embedding = nn.Embedding(vocab_size, size)
        self.out = nn.Linear(size, 2)
        self.left = nn.Linear(size, 5 * size)
        self.right = nn.Linear(size, 5 * size)
        self.from_word = nn.Linear(size, size, bias=False)
        self.from_children = nn.Linear(size, size, bias=False)
        self.from_word.weight = nn.Parameter(torch.eye(size))
        self.from_children.weight = nn.Parameter(torch.eye(size))
    
    #The following code is very similar to the forward function of a vanilla LSTM cell.
    def process_children(self, left_h, left_c, right_h, right_c, word_idx):
        word_vec = self.embedding(word_idx)
        lstm_in = self.left(left_h) + self.right(right_h)
        
        #Note we now have two forget gates f1 and f2 for left and right children.
        a, i, f1, f2, o = lstm_in.chunk(5, 1)
        c = a.tanh() * i.sigmoid() + f1.sigmoid()*left_c + f2.sigmoid()*right_c
        
        #We take a combination of the output from the children and the output from
        #the word vector from the node itself to get the output hidden state.
        h = self.from_children(o.sigmoid() * c.tanh()) + \
            self.from_word(word_vec)
        return h, c
    
    def leaf(self, word_idx):
        return self.embedding(word_idx), Variable(torch.cuda.FloatTensor(word_idx.size()[0], self.size).zero_())

    def logits(self, encoding):
        return self.out(encoding)

#The following uses torchfold in order to build the computational graphs for the input trees.
def encode_tree_fold(fold, tree):
    def encode_node(node):
        if node.is_leaf():
            #Split two ways, one for hidden state and one for cell state.
            return fold.add('leaf', (int(node.val),)).split(2)
        else:
            children_states = []
            for child in node.children:
                h, c = encode_node(child)
                children_states += [h, c]
                
            #Add the index of the node's word at the end.
            children_states.append(int(node.val))
            
            #Split two ways, one for hidden state and one for cell state.
            return fold.add('process_children', tuple(children_states)).split(2)
    encoding, _ = encode_node(tree)
    return fold.add('logits', (encoding,))

def batch_update_recursive(fold, batch, model, optimizer):
    all_logits, all_labels = [], []
    for tree, label in batch:
        all_logits.append(encode_tree_fold(fold, tree))
        all_labels.append(label)
        
    #Clear grads before updating parameters.
    optimizer.zero_grad()
    res = fold.apply(model, all_logits)
    criterion = nn.CrossEntropyLoss()
    loss = criterion(res[0], Variable(torch.cuda.LongTensor(all_labels)))
    loss.backward()
    optimizer.step()
    return loss

def validate(fold, batch, model):
    test_logits, test_labels = [], []

    for tree, label in batch:
        test_logits.append(encode_tree_fold(fold, tree))
        test_labels.append(label)
    res = fold.apply(model, test_logits)
    
    #Get prediction by picking the label with highest probability.
    _, predicted = torch.max(res[0], 1)
    
    #Get the number of correct predictions
    num_correct = (predicted == Variable(torch.cuda.LongTensor(test_labels))).sum().data[0]
    return num_correct
