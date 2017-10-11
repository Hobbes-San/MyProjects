import util
import time
import json
import torch
from torch import optim
from pytorch_tools_master.pytorch_tools import torchfold_Alt
from random import shuffle

#This program loads the Java trees into the data list, splits it into training
#and testing sets, then trains for several epochs, measuring the testing accuracy
#at the end of each epoch.
print (time.localtime())

Java_data = []

#Load the data.
with open('indexed_trees_labeled_Java.jsonl', 'r') as f:
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
        Java_data.append((tree_list, label))
        line_count += 1
        if line_count % 500 == 0:
            print (line_count)

print ('Done with reading data')

print (time.localtime())

shuffle(Java_data); print ('Data size: ' + str(len(Java_data)))

#Split into training and testing sets, making sure to keep a single persons's
#code solutions either all in the training set or all in the testing set to
#prevent data leakage.
Java_total_size = len(Java_data); Java_train_size = int(Java_total_size*(4/5))
Java_test_size = Java_total_size - Java_train_size
Java_train_data = []; Java_test_data = []
for i in range(Java_train_size):
    label = Java_data[i][1]
    for tree in Java_data[i][0]:
        Java_train_data.append((tree, label))
for i in range(Java_train_size, Java_total_size):
    label = Java_data[i][1]
    for tree in Java_data[i][0]:        
        Java_test_data.append((tree, label))

shuffle(Java_train_data); shuffle(Java_test_data)

load_previous = False

#77 is the number of different types of expressions in Java (i.e. vocabulary size for Java).
#50 is the embedding dimension.
java_model = util.RecursiveModel(77, 50); java_model.cuda()

if load_previous:
    print ('Loaded')
    java_model.load_state_dict(torch.load('java_checkpoint_Alt.pth'))
java_optimizer = optim.Adagrad(java_model.parameters(), lr=0.01, weight_decay=0.001)

epochs = 10; prev_accuracy = 50
for epoch in range(epochs):
    shuffle (Java_train_data)
    batch = []; count = 0
    for tree, label in Java_train_data:
        if len(batch) >= 50:
            
            #Here we create a new fold everytime we process a new batch so that we don't
            #use additional memory by keeping results from old batches around.
            count += 1; java_fold = torchfold_Alt.Fold(); java_fold.volatile = False
            loss = util.batch_update_recursive(java_fold, batch, java_model, java_optimizer)
            batch = []
        batch.append((tree, label))
        
    if len(batch) > 0:
        java_fold = torchfold_Alt.Fold(); java_fold.volatile = False
        util.batch_update_recursive(java_fold, batch, java_model, java_optimizer)
    
    count_ = 0; batch_ = []; total_correct = 0
    for tree, label in Java_test_data:
        if len(batch_) >= 50:
            
            #Here we create a new fold everytime we process a new batch so that we don't
            #use additional memory by keeping results from old batches around.
            count_ += 1; java_fold = torchfold_Alt.Fold(); java_fold.volatile = True
            num = util.validate(java_fold, batch_, java_model)
            total_correct += num
            batch_ = []
        batch_.append((tree, label))
    
    if len(batch_) > 0:
        java_fold = torchfold_Alt.Fold(); java_fold.volatile = True
        num = util.validate(java_fold, batch_, java_model); total_correct += num
    
    accuracy = total_correct/len(Java_test_data)*100.0
    print (' '.join(['Epoch:', str(epoch), 'Final Accuracy:', str(accuracy), '%']))
    print (time.localtime())
    
    #If the accuracy is better than the best accuracy so far, write down the training
    #and testing data as JSON files and save the parameters of the model.
    if accuracy > prev_accuracy:
        with open('indexed_trees_labeled_Java_Train_Alt.jsonl', 'w') as f:
            for tree, label in Java_train_data:
                r = []; util.serialize(tree, r)
                f.write(json.dumps({'hired': label, 'solution': r, 'language': 'Java'}) + '\n')
        with open('indexed_trees_labeled_Java_Test_Alt.jsonl', 'w') as f:
            for tree, label in Java_test_data:
                r = []; util.serialize(tree, r)
                f.write(json.dumps({'hired': label, 'solution': r, 'language': 'Java'}) + '\n')
        torch.save(java_model.state_dict(), 'java_checkpoint_Alt.pth')
        prev_accuracy = accuracy
