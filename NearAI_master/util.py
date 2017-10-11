import javalang_master.javalang
import clang_38.clang.cindex

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

idx2word = idx2word_Cpp + idx2word_Java
word2idx = {}
for i in range(len(idx2word)):
    word2idx[idx2word[i]] = i

n_words = len(idx2word)

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
