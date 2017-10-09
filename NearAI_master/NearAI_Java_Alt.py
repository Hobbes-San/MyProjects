import util
import time
import json
import torch
from torch import nn
from torch import optim
from torch.autograd import Variable
from pytorch_tools_master.pytorch_tools import torchfold_Alt
from random import shuffle

idx2word_Cpp = [
'CursorKind.UNEXPOSED_DECL',
'CursorKind.STRUCT_DECL',
'CursorKind.UNION_DECL',
'CursorKind.CLASS_DECL',
'CursorKind.ENUM_DECL',
'CursorKind.FIELD_DECL',
'CursorKind.ENUM_CONSTANT_DECL',
'CursorKind.FUNCTION_DECL',
'CursorKind.VAR_DECL',
'CursorKind.PARM_DECL',
'CursorKind.OBJC_INTERFACE_DECL',
'CursorKind.OBJC_CATEGORY_DECL',
'CursorKind.OBJC_PROTOCOL_DECL',
'CursorKind.OBJC_PROPERTY_DECL',
'CursorKind.OBJC_IVAR_DECL',
'CursorKind.OBJC_INSTANCE_METHOD_DECL',
'CursorKind.OBJC_CLASS_METHOD_DECL',
'CursorKind.OBJC_IMPLEMENTATION_DECL',
'CursorKind.OBJC_CATEGORY_IMPL_DECL',
'CursorKind.TYPEDEF_DECL',
'CursorKind.CXX_METHOD',
'CursorKind.NAMESPACE',
'CursorKind.LINKAGE_SPEC',
'CursorKind.CONSTRUCTOR',
'CursorKind.DESTRUCTOR',
'CursorKind.CONVERSION_FUNCTION',
'CursorKind.TEMPLATE_TYPE_PARAMETER',
'CursorKind.TEMPLATE_NON_TYPE_PARAMETER',
'CursorKind.TEMPLATE_TEMPLATE_PARAMETER',
'CursorKind.FUNCTION_TEMPLATE',
'CursorKind.CLASS_TEMPLATE',
'CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION',
'CursorKind.NAMESPACE_ALIAS',
'CursorKind.USING_DIRECTIVE',
'CursorKind.USING_DECLARATION',
'CursorKind.TYPE_ALIAS_DECL',
'CursorKind.OBJC_SYNTHESIZE_DECL',
'CursorKind.OBJC_DYNAMIC_DECL',
'CursorKind.CXX_ACCESS_SPEC_DECL',
'CursorKind.OBJC_SUPER_CLASS_REF',
'CursorKind.OBJC_PROTOCOL_REF',
'CursorKind.OBJC_CLASS_REF',
'CursorKind.TYPE_REF',
'CursorKind.CXX_BASE_SPECIFIER',
'CursorKind.TEMPLATE_REF',
'CursorKind.NAMESPACE_REF',
'CursorKind.MEMBER_REF',
'CursorKind.LABEL_REF',
'CursorKind.OVERLOADED_DECL_REF',
'CursorKind.VARIABLE_REF',
'CursorKind.INVALID_FILE',
'CursorKind.NO_DECL_FOUND',
'CursorKind.NOT_IMPLEMENTED',
'CursorKind.INVALID_CODE',
'CursorKind.UNEXPOSED_EXPR',
'CursorKind.DECL_REF_EXPR',
'CursorKind.MEMBER_REF_EXPR',
'CursorKind.CALL_EXPR',
'CursorKind.OBJC_MESSAGE_EXPR',
'CursorKind.BLOCK_EXPR',
'CursorKind.INTEGER_LITERAL',
'CursorKind.FLOATING_LITERAL',
'CursorKind.IMAGINARY_LITERAL',
'CursorKind.STRING_LITERAL',
'CursorKind.CHARACTER_LITERAL',
'CursorKind.PAREN_EXPR',
'CursorKind.UNARY_OPERATOR',
'CursorKind.ARRAY_SUBSCRIPT_EXPR',
'CursorKind.BINARY_OPERATOR',
'CursorKind.COMPOUND_ASSIGNMENT_OPERATOR',
'CursorKind.CONDITIONAL_OPERATOR',
'CursorKind.CSTYLE_CAST_EXPR',
'CursorKind.COMPOUND_LITERAL_EXPR',
'CursorKind.INIT_LIST_EXPR',
'CursorKind.ADDR_LABEL_EXPR',
'CursorKind.StmtExpr',
'CursorKind.GENERIC_SELECTION_EXPR',
'CursorKind.GNU_NULL_EXPR',
'CursorKind.CXX_STATIC_CAST_EXPR',
'CursorKind.CXX_DYNAMIC_CAST_EXPR',
'CursorKind.CXX_REINTERPRET_CAST_EXPR',
'CursorKind.CXX_CONST_CAST_EXPR',
'CursorKind.CXX_FUNCTIONAL_CAST_EXPR',
'CursorKind.CXX_TYPEID_EXPR',
'CursorKind.CXX_BOOL_LITERAL_EXPR',
'CursorKind.CXX_NULL_PTR_LITERAL_EXPR',
'CursorKind.CXX_THIS_EXPR',
'CursorKind.CXX_THROW_EXPR',
'CursorKind.CXX_NEW_EXPR',
'CursorKind.CXX_DELETE_EXPR',
'CursorKind.CXX_UNARY_EXPR',
'CursorKind.OBJC_STRING_LITERAL',
'CursorKind.OBJC_ENCODE_EXPR',
'CursorKind.OBJC_SELECTOR_EXPR',
'CursorKind.OBJC_PROTOCOL_EXPR',
'CursorKind.OBJC_BRIDGE_CAST_EXPR',
'CursorKind.PACK_EXPANSION_EXPR',
'CursorKind.SIZE_OF_PACK_EXPR',
'CursorKind.LAMBDA_EXPR'
'CursorKind.OBJ_BOOL_LITERAL_EXPR',
'CursorKind.OBJ_SELF_EXPR',
'CursorKind.UNEXPOSED_STMT',
'CursorKind.LABEL_STMT',
'CursorKind.COMPOUND_STMT',
'CursorKind.CASE_STMT',
'CursorKind.DEFAULT_STMT',
'CursorKind.IF_STMT',
'CursorKind.SWITCH_STMT',
'CursorKind.WHILE_STMT',
'CursorKind.DO_STMT',
'CursorKind.FOR_STMT',
'CursorKind.GOTO_STMT',
'CursorKind.INDIRECT_GOTO_STMT',
'CursorKind.CONTINUE_STMT',
'CursorKind.BREAK_STMT',
'CursorKind.RETURN_STMT',
'CursorKind.ASM_STMT',
'CursorKind.OBJC_AT_TRY_STMT',
'CursorKind.OBJC_AT_CATCH_STMT',
'CursorKind.OBJC_AT_FINALLY_STMT',
'CursorKind.OBJC_AT_THROW_STMT',
'CursorKind.OBJC_AT_SYNCHRONIZED_STMT',
'CursorKind.OBJC_AUTORELEASE_POOL_STMT',
'CursorKind.OBJC_FOR_COLLECTION_STMT',
'CursorKind.CXX_CATCH_STMT',
'CursorKind.CXX_TRY_STMT',
'CursorKind.CXX_FOR_RANGE_STMT',
'CursorKind.SEH_TRY_STMT',
'CursorKind.SEH_EXCEPT_STMT',
'CursorKind.SEH_FINALLY_STMT',
'CursorKind.MS_ASM_STMT',
'CursorKind.NULL_STMT',
'CursorKind.DECL_STMT',
'CursorKind.TRANSLATION_UNIT',
'CursorKind.UNEXPOSED_ATTR',
'CursorKind.IB_ACTION_ATTR',
'CursorKind.IB_OUTLET_ATTR',
'CursorKind.IB_OUTLET_COLLECTION_ATTR',
'CursorKind.CXX_FINAL_ATTR',
'CursorKind.CXX_OVERRIDE_ATTR',
'CursorKind.ANNOTATE_ATTR',
'CursorKind.ASM_LABEL_ATTR',
'CursorKind.PACKED_ATTR',
'CursorKind.PURE_ATTR',
'CursorKind.CONST_ATTR',
'CursorKind.NODUPLICATE_ATTR',
'CursorKind.CUDACONSTANT_ATTR',
'CursorKind.CUDADEVICE_ATTR',
'CursorKind.CUDAGLOBAL_ATTR',
'CursorKind.CUDAHOST_ATTR',
'CursorKind.CUDASHARED_ATTR',
'CursorKind.VISIBILITY_ATTR',
'CursorKind.DLLEXPORT_ATTR',
'CursorKind.DLLIMPORT_ATTR',
'CursorKind.PREPROCESSING_DIRECTIVE',
'CursorKind.MACRO_DEFINITION',
'CursorKind.MACRO_INSTANTIATION',
'CursorKind.INCLUSION_DIRECTIVE',
'CursorKind.MODULE_IMPORT_DECL',
'CursorKind.TYPE_ALIAS_TEMPLATE_DECL'
]

idx2word_java = [
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

idx2word = idx2word_Cpp + idx2word_java
java_word2idx = {}; Cpp_word2idx = {}
for i in range(len(idx2word_java)):
    java_word2idx[idx2word_java[i]] = i
for i in range(len(idx2word_Cpp)):
    Cpp_word2idx[idx2word_Cpp[i]] = i

print (time.localtime())

java_data = []; Cpp_data = []

with open('indexed_trees_labeled.jsonl', 'r') as f:
    line_count = 0
    for line in f:
        d = json.loads(line)
        label = d['hired']
        if label == 2:
            label = 1
        code_serialized = d['solution']
        language = d['lang']
        indexed_tree = util.Node(); indexed_tree.val = code_serialized[0]
        stack = [indexed_tree]; util.deserialize(code_serialized, stack)
        if language == 'java':
            java_data.append((indexed_tree, label))
        #else:
        #    Cpp_data.append((indexed_tree, label))
        line_count += 1
        if line_count % 10000 == 0:
            print (line_count)

print ('Done with reading data')

print (time.localtime())

shuffle(java_data); java_data = java_data[:100]
java_total_size = len(java_data); java_train_size = int(java_total_size*(4/5))
java_test_size = java_total_size - java_train_size

java_train_data = java_data[:java_train_size]; java_test_data = java_data[java_train_size:]

"""Cpp_total_size = len(Cpp_data); Cpp_train_size = int(Cpp_total_size*(4/5))
Cpp_test_size = Cpp_total_size - Cpp_train_size

java_train_data = java_data[:java_train_size]; java_test_data = java_data[java_train_size:]
Cpp_train_data = Cpp_data[:java_train_size]; Cpp_test_data = Cpp_data[java_train_size:]"""

"""class BoWClassifier(nn.Module):
    
    def __init__(self):
        super(BoWClassifier, self).__init__()
        self.linear = nn.Linear(236, 2)
    
    def forward(self, x):
        return torch.nn.functional.log_softmax(self.linear(x))

bc = BoWClassifier()
loss_BoW = nn.NLLLoss()
optimizer = optim.SGD(bc.parameters(), lr = 0.1)

for epoch in range(10):
    correct = 0
    for tree, label in train_data:
        bc.zero_grad()
        x = torch.cuda.zeros(236)
        for node in tree.traverse():
            x[int(node.val)] += 1
        x = Variable(x.view(1, -1))
        y = Variable(torch.cuda.LongTensor([label]))
        
        log_probs = bc.forward(x)
        
        loss = loss_BoW(log_probs, y)
        loss.backward()
        optimizer.step()
    
    for tree, label in test_data:
        x = torch.cuda.zeros(236)
        for node in tree.traverse():
            x[int(node.val)] += 1
        x = Variable(x.view(1, -1))
        y = Variable(torch.cuda.LongTensor([label]))
        
        log_probs = bc.forward(x)
        _, predicted = torch.max(log_probs, 1)
        correct += (predicted == y).data[0]
        
    percentage = correct/len(test_data)*100.0
    print (("Epoch: %d Correct Rate Percentage: %f") % (epoch, percentage))
    print (time.localtime())"""

"""class TreeLSTM(nn.Module):
    def __init__(self, num_units):
        super(TreeLSTM, self).__init__()
        self.num_units = num_units
        self.left = nn.Linear(num_units, 5 * num_units)
        self.right = nn.Linear(num_units, 5 * num_units)
        self.from_word = Variable(torch.randn(1).cuda()*torch.eye(self.num_units).cuda())
        self.from_children = Variable(torch.randn(1).cuda()*torch.eye(self.num_units).cuda())
        
    def forward(self, word_vec, left_h, left_c, right_h, right_c):
        lstm_in = self.left(left_h) + self.right(right_h)
        a, i, f1, f2, o = lstm_in.chunk(5, 1)
        c = a.tanh() * i.sigmoid() + f1.sigmoid()*left_c + f2.sigmoid()*right_c
        h = torch.mm(o.sigmoid() * c.tanh(), self.from_children) + \
            torch.mm(word_vec, self.from_word)
        return h, c
    
    def forward(self, inputs):
        m = len(inputs)
        lstm_in = self.left(inputs[0][0])
        for i in range(1, m):
            r = i/(m-1); l = 1-r
            lstm_in += (l * self.left(inputs[i][0]) + r * self.right(inputs[i][0]))
        a, i, f1, f2, o = lstm_in.chunk(5, 1)
        c = a.tanh() * i.sigmoid() + f1.sigmoid() * inputs[0][1]
        for i in range(1, m):
            r = i/(m-1); l = 1-r
            c += ((l * f1 + r * f2).sigmoid() * inputs[i][1])
        h = o.sigmoid() * c.tanh()
        return h, c"""

class RecursiveModel(nn.Module):

    def __init__(self, vocab_size, size):
        super(RecursiveModel, self).__init__()
        self.volatile = False
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
        
    def process_children(self, left_h, left_c, right_h, right_c, word_idx):
        word_vec = self.embedding(word_idx)
        lstm_in = self.left(left_h) + self.right(right_h)
        a, i, f1, f2, o = lstm_in.chunk(5, 1)
        c = a.tanh() * i.sigmoid() + f1.sigmoid()*left_c + f2.sigmoid()*right_c
        h = self.from_children(o.sigmoid() * c.tanh()) + \
            self.from_word(word_vec)
        return h, c
    
    def leaf(self, word_idx):
        return self.embedding(word_idx), Variable(torch.cuda.FloatTensor(word_idx.size()[0], self.size).zero_())

    def logits(self, encoding):
        return self.out(encoding)

def encode_tree_fold(fold, tree):
    def encode_node(node):
        if node.is_leaf():
            return fold.add('leaf', (int(node.val),)).split(2)
        else:
            children_states = []
            for child in node.children:
                h, c = encode_node(child)
                children_states += [h, c]
            children_states.append(int(node.val))
            return fold.add('process_children', tuple(children_states)).split(2)
    encoding, _ = encode_node(tree)
    return fold.add('logits', (encoding,))

def batch_update_recursive(fold, batch, model, optimizer):
    all_logits, all_labels = [], []
    for tree, label in batch:
        all_logits.append(encode_tree_fold(fold, tree))
        all_labels.append(label)
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
    _, predicted = torch.max(res[0], 1)
    num_correct = (predicted == Variable(torch.cuda.LongTensor(test_labels))).sum().data[0]
    return num_correct

load_previous = False
java_model = RecursiveModel(len(java_word2idx), 25); java_model.cuda()
#Cpp_model = RecursiveModel(len(Cpp_word2idx), 25); Cpp_model.cuda()

if load_previous:
    print ('Loaded')
    java_model.load_state_dict(torch.load('java_checkpoint.pth'))
    #Cpp_model.load_state_dict(torch.load('Cpp_checkpoint.pth'))
java_optimizer = optim.Adagrad(java_model.parameters(), lr=0.01, weight_decay=0.001)
#Cpp_optimizer = optim.Adagrad(Cpp_model.parameters(), lr=0.001, weight_decay=0.01)
java_fold = torchfold_Alt.Fold(); #Cpp_fold = torchfold.Fold()

epochs = 1
for epoch in range(epochs):
    shuffle (java_train_data)
    batch = []; count = 0; java_fold.volatile = False
    for tree, label in java_train_data:
        if len(batch) >= 50:
            count += 1
            loss = batch_update_recursive(java_fold, batch, java_model, java_optimizer)
            if count % 20 == 0:
                print (' '.join(['Epoch:', str(epoch), 'Batch:', str(count), 'Loss:', str(loss.data[0])]))
                print (time.localtime())
            batch = []
        batch.append((tree, label))
        
    if len(batch) > 0:
        batch_update_recursive(java_fold, batch, java_model, java_optimizer)
    
    count_ = 0; batch_ = []; total_correct = 0; java_fold.volatile = True
    for tree, label in java_test_data:
        if len(batch_) >= 50:
            count_ += 1; num = validate(java_fold, batch_, java_model)
            total_correct += num
            if count_ % 20 == 0:
                print (' '.join(['Number of Correct Predictions from Batch:', str(count_), str(num)]))
                print (time.localtime())
            batch_ = []
        batch_.append((tree, label))
    
    if len(batch_) > 0:
        num = validate(java_fold, batch_, java_model); total_correct += num
    
    prev_accuracy = 50
    accuracy = total_correct/len(java_test_data)*100.0
    print (''.join(['Epoch:', str(epoch), 'Final Accuracy: ', str(accuracy), '%']))
    print (time.localtime())
    
    if accuracy > prev_accuracy:
        torch.save(java_model.state_dict(), 'java_checkpoint.pth')
    
    prev_accuracy = accuracy