import time
import json
from lime.lime_text import LimeTextExplainer
import sklearn
from sklearn import feature_extraction
from sklearn import pipeline
from collections import defaultdict

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

Cpp_word2idx = {}
for i in range(len(idx2word_Cpp)):
    Cpp_word2idx[idx2word_Cpp[i]] = i

print (time.localtime())

Cpp_train_data = []; Cpp_test_data = []; Cpp_train_labels = []; Cpp_test_labels = []

with open('indexed_trees_labeled_Cpp_Train_Alt.jsonl', 'r') as f:
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
                word_list.append(idx2word_Cpp[int(index)][11:])
        sentence = ' '.join(word_list)
        Cpp_train_data.append(sentence)
        Cpp_train_labels.append(label)
        line_count += 1
        if line_count % 10000 == 0:
            print (line_count)

with open('indexed_trees_labeled_Cpp_Test_Alt.jsonl', 'r') as f:
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
                word_list.append(idx2word_Cpp[int(index)][11:])
        sentence = ' '.join(word_list)
        Cpp_test_data.append(sentence)
        Cpp_test_labels.append(label)
        line_count += 1
        if line_count % 10000 == 0:
            print (line_count)

print ('Done with reading data')

print (time.localtime())

vectorizer = feature_extraction.text.CountVectorizer()
train_vectors = vectorizer.fit_transform(Cpp_train_data)
test_vectors = vectorizer.transform(Cpp_test_data)

lr = sklearn.linear_model.LogisticRegression()
lr.fit(train_vectors, Cpp_train_labels)
accuracy = 100.0*lr.score(test_vectors, Cpp_test_labels)
print(' '.join(['C++ BoW Logistic Regression Accuracy:', str(accuracy), '%']))

#The following is an example of LIME telling us which words were most important
#in the model coming up with prediction probabilities for a particular code.
"""c = pipeline.make_pipeline(vectorizer, lr)

with open('C++Test_Sentence', 'r') as f:
    test_sentence = f.read()

D = defaultdict(int)
for word in test_sentence.split():
    D[word] += 1

print(D)

print (c.predict_proba([test_sentence]))
explainer = LimeTextExplainer()
exp = explainer.explain_instance(test_sentence, c.predict_proba, num_features=100)
print (exp.as_list())"""