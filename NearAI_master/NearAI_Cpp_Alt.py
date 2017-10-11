import util
import time
import json
import torch
from torch import nn
from torch import optim
from torch.autograd import Variable
from pytorch_tools_master.pytorch_tools import torchfold_Alt
from random import shuffle

#This program loads the C++ trees into the data list, splits it into training
#and testing sets, then trains for several epochs, measuring the testing accuracy
#at the end of each epoch.
print (time.localtime())

Cpp_data = []

#Load the data.
with open('indexed_trees_labeled_Cpp.jsonl', 'r') as f:
    line_count = 0
    for line in f:
        d = json.loads(line)
        label = d['hired']
        if label == 2:
            label = 1
        serialized_list = d['solutions']; tree_list = []
        for code_serialized in serialized_list:
            indexed_tree = util.Node(); indexed_tree.val = code_serialized[0]
            stack = [indexed_tree]; util.deserialize(code_serialized, stack)
            tree_list.append(indexed_tree)
        Cpp_data.append((tree_list, label))
        line_count += 1
        if line_count % 500 == 0:
            print (line_count)

print ('Done with reading data')

print (time.localtime())

shuffle(Cpp_data); print ('Data size: ' + str(len(Cpp_data)))

#Split into training and testing sets, making sure to keep a single persons's
#code solutions either all in the training set or all in the testing set to
#prevent data leakage.
Cpp_total_size = len(Cpp_data); Cpp_train_size = int(Cpp_total_size*(4/5))
Cpp_test_size = Cpp_total_size - Cpp_train_size
Cpp_train_data = []; Cpp_test_data = []
for i in range(Cpp_train_size):
    label = Cpp_data[i][1]
    for tree in Cpp_data[i][0]:
        Cpp_train_data.append((tree, label))
for i in range(Cpp_train_size, Cpp_total_size):
    label = Cpp_data[i][1]
    for tree in Cpp_data[i][0]:        
        Cpp_test_data.append((tree, label))
        
shuffle(Cpp_train_data); shuffle(Cpp_test_data)

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

load_previous = False

#159 is the number of different types of expressions in C++ (i.e. vocabulary size for C++).
#100 is the embedding dimension.
Cpp_model = RecursiveModel(159, 100); Cpp_model.cuda()

if load_previous:
    print ('Loaded')
    Cpp_model.load_state_dict(torch.load('Cpp_checkpoint_Alt.pth'))
Cpp_optimizer = optim.Adagrad(Cpp_model.parameters(), lr=0.01, weight_decay=0.001)

epochs = 10; prev_accuracy = 50
for epoch in range(epochs):
    shuffle (Cpp_train_data)
    batch = []; count = 0
    for tree, label in Cpp_train_data:
        if len(batch) >= 50:
            
            #Here we create a new fold everytime we process a new batch so that we don't
            #use additional memory by keeping results from old batches around.
            count += 1; Cpp_fold = torchfold_Alt.Fold(); Cpp_fold.volatile = False
            loss = batch_update_recursive(Cpp_fold, batch, Cpp_model, Cpp_optimizer)
            batch = []
        batch.append((tree, label))
        
    if len(batch) > 0:
        Cpp_fold = torchfold_Alt.Fold(); Cpp_fold.volatile = False
        batch_update_recursive(Cpp_fold, batch, Cpp_model, Cpp_optimizer)
    
    count_ = 0; batch_ = []; total_correct = 0
    for tree, label in Cpp_test_data:
        if len(batch_) >= 50:
            
            #Here we create a new fold everytime we process a new batch so that we don't
            #use additional memory by keeping results from old batches around.
            count_ += 1; Cpp_fold = torchfold_Alt.Fold(); Cpp_fold.volatile = True
            num = validate(Cpp_fold, batch_, Cpp_model)
            total_correct += num
            batch_ = []
        batch_.append((tree, label))
    
    if len(batch_) > 0:
        Cpp_fold = torchfold_Alt.Fold(); Cpp_fold.volatile = True
        num = validate(Cpp_fold, batch_, Cpp_model); total_correct += num
    
    accuracy = total_correct/len(Cpp_test_data)*100.0
    print (' '.join(['Epoch:', str(epoch), 'Final Accuracy:', str(accuracy), '%']))
    print (time.localtime())
    
    #If the accuracy is better than the best accuracy so far, write down the training
    #and testing data as JSON files and save the parameters of the model.
    if accuracy > prev_accuracy:
        with open('indexed_trees_labeled_Cpp_Train_Alt.jsonl', 'w') as f:
            for tree, label in Cpp_train_data:
                r = []; util.serialize(tree, r)
                f.write(json.dumps({'hired': label, 'solution': r, 'language': 'C++'}) + '\n')
        with open('indexed_trees_labeled_Cpp_Test_Alt.jsonl', 'w') as f:
            for tree, label in Cpp_test_data:
                r = []; util.serialize(tree, r)
                f.write(json.dumps({'hired': label, 'solution': r, 'language': 'C++'}) + '\n')
        torch.save(Cpp_model.state_dict(), 'Cpp_checkpoint_Alt.pth')
        prev_accuracy = accuracy
