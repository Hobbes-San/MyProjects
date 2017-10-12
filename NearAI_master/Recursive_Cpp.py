import util
import time
import json
import torch
from torch import optim
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

load_previous = False

#159 is the number of different types of expressions in C++ (i.e. vocabulary size for C++).
#100 is the embedding dimension.
Cpp_model = util.RecursiveModel(159, 100); Cpp_model.cuda()

if load_previous:
    print ('Loaded')
    Cpp_model.load_state_dict(torch.load('Cpp_checkpoint_Alt.pth'))
Cpp_optimizer = optim.Adagrad(Cpp_model.parameters(), lr=0.001, weight_decay=0.001)

epochs = 10; prev_accuracy = 50
for epoch in range(epochs):
    shuffle (Cpp_train_data)
    batch = []; count = 0
    for tree, label in Cpp_train_data:
        if len(batch) >= 50:
            
            #Here we create a new fold everytime we process a new batch so that we don't
            #use additional memory by keeping results from old batches around.
            count += 1; Cpp_fold = torchfold_Alt.Fold(); Cpp_fold.volatile = False
            loss = util.batch_update_recursive(Cpp_fold, batch, Cpp_model, Cpp_optimizer)
            batch = []
        batch.append((tree, label))
        
    if len(batch) > 0:
        Cpp_fold = torchfold_Alt.Fold(); Cpp_fold.volatile = False
        util.batch_update_recursive(Cpp_fold, batch, Cpp_model, Cpp_optimizer)
    
    count_ = 0; batch_ = []; total_correct = 0
    for tree, label in Cpp_test_data:
        if len(batch_) >= 50:
            
            #Here we create a new fold everytime we process a new batch so that we don't
            #use additional memory by keeping results from old batches around.
            count_ += 1; Cpp_fold = torchfold_Alt.Fold(); Cpp_fold.volatile = True
            num = util.validate(Cpp_fold, batch_, Cpp_model)
            total_correct += num
            batch_ = []
        batch_.append((tree, label))
    
    if len(batch_) > 0:
        Cpp_fold = torchfold_Alt.Fold(); Cpp_fold.volatile = True
        num = util.validate(Cpp_fold, batch_, Cpp_model); total_correct += num
    
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
