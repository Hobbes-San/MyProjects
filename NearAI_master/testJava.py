import util
import time
import json
import torch
from pytorch_tools_master.pytorch_tools import torchfold_Alt
import NearAI_Java_Alt

#This is a testing program for Java code classification.
print (time.localtime())

java_test_data = []

with open('indexed_trees_labeled_Java_Test_Alt.jsonl', 'r') as f:
    line_count = 0
    for line in f:
        d = json.loads(line)
        label = d['hired']
        if label == 2:
            label = 1
        code_serialized = d['solution']
        indexed_tree = util.Node(); indexed_tree.val = code_serialized[0]
        stack = [indexed_tree]; util.deserialize(code_serialized, stack)
        java_test_data.append((indexed_tree, label))
        line_count += 1
        if line_count % 10000 == 0:
            print (line_count)

print ('Done with reading data')

print (time.localtime())

#Load the saved parameters.
java_model = NearAI_Java_Alt.RecursiveModel(77, 50); java_model.cuda()
java_model.load_state_dict(torch.load('java_checkpoint_Alt.pth'))

epochs = 1
for epoch in range(epochs):
    count_ = 0; batch_ = []; total_correct = 0
    for tree, label in java_test_data:
        if len(batch_) >= 50:
            count_ += 1; java_fold = torchfold_Alt.Fold(); java_fold.volatile = True
            num = NearAI_Java_Alt.validate(java_fold, batch_, java_model)
            total_correct += num
            batch_ = []
        batch_.append((tree, label))
    
    if len(batch_) > 0:
        java_fold = torchfold_Alt.Fold(); java_fold.volatile = True
        num = NearAI_Java_Alt.validate(java_fold, batch_, java_model); total_correct += num
    
    accuracy = total_correct/len(java_test_data)*100.0
    print (' '.join(['Epoch:', str(epoch), 'Final Accuracy:', str(accuracy), '%']))
    print (time.localtime())