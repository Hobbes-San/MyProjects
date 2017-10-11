import time
import json
from lime.lime_text import LimeTextExplainer
import sklearn
from sklearn import feature_extraction
from sklearn import pipeline
from collections import defaultdict

idx2word_Java = [
'CompilationUnit',
'Import',
'Documented',
'Declaration',
'TypeDeclaration',
'PackageDeclaration',
'ClassDeclaration',
'EnumDeclaration',
'InterfaceDeclaration',
'AnnotationDeclaration',
'Type',
'BasicType',
'ReferenceType',
'TypeArgument',
'TypeParameter',
'Annotation',
'ElementValuePair',
'ElementArrayValue',
'Member',
'MethodDeclaration',
'FieldDeclaration',
'ConstructorDeclaration',
'ConstantDeclaration',
'ArrayInitializer',
'VariableDeclaration',
'LocalVariableDeclaration',
'VariableDeclarator',
'FormalParameter',
'InferredFormalParameter',
'Statement',
'IfStatement',
'WhileStatement',
'DoStatement',
'ForStatement',
'AssertStatement',
'BreakStatement',
'ContinueStatement',
'ReturnStatement',
'ThrowStatement',
'SynchronizedStatement',
'TryStatement',
'SwitchStatement',
'BlockStatement',
'StatementExpression',
'TryResource',
'CatchClause',
'CatchClauseParameter',
'SwitchStatementCase',
'ForControl',
'EnhancedForControl',
'Expression',
'Assignment',
'TernaryExpression',
'BinaryOperation',
'Cast',
'MethodReference',
'LambdaExpression',
'Primary',
'Literal',
'This',
'MemberReference',
'Invocation',
'ExplicitConstructorInvocation',
'SuperConstructorInvocation',
'MethodInvocation',
'SuperMethodInvocation',
'SuperMemberReference',
'ArraySelector',
'ClassReference',
'VoidClassReference',
'Creator',
'ArrayCreator',
'ClassCreator',
'InnerClassCreator',
'EnumBody',
'EnumConstantDeclaration',
'AnnotationMethod'
]

Java_word2idx = {}
for i in range(len(idx2word_Java)):
    Java_word2idx[idx2word_Java[i]] = i
    
print (time.localtime())

java_train_data = []; java_test_data = []; java_train_labels = []; java_test_labels = []

with open('indexed_trees_labeled_Java_Train_Alt.jsonl', 'r') as f:
    line_count = 0
    for line in f:
        d = json.loads(line)
        label = d['hired']
        if label == 2:
            label = 1
        code_serialized = d['solution']
        word_list = []
        for index in code_serialized:
            if index != ')' and index != 0:
                word_list.append(idx2word_Java[int(index)])
        sentence = ' '.join(word_list)
        java_train_data.append(sentence)
        java_train_labels.append(label)
        line_count += 1
        if line_count % 10000 == 0:
            print (line_count)

with open('indexed_trees_labeled_Java_Test_Alt.jsonl', 'r') as f:
    line_count = 0
    for line in f:
        d = json.loads(line)
        label = d['hired']
        if label == 2:
            label = 1
        code_serialized = d['solution']
        word_list = []
        for index in code_serialized:
            if index != ')' and index != 132:
                word_list.append(idx2word_Java[int(index)])
        sentence = ' '.join(word_list)
        java_test_data.append(sentence)
        java_test_labels.append(label)
        line_count += 1
        if line_count % 10000 == 0:
            print (line_count)

print ('Done with reading data')

print (time.localtime())

vectorizer = feature_extraction.text.CountVectorizer()
train_vectors = vectorizer.fit_transform(java_train_data)
test_vectors = vectorizer.transform(java_test_data)

lr = sklearn.linear_model.LogisticRegression()
lr.fit(train_vectors, java_train_labels)
accuracy = 100.0*lr.score(test_vectors, java_test_labels)
print(' '.join(['Java BoW Logistic Regression Accuracy:', str(accuracy), '%']))
c = pipeline.make_pipeline(vectorizer, lr)