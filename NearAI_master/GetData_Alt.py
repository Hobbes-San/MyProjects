import javalang_master.javalang
import json
import util

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

java_word2idx = {}; Cpp_word2idx = {}
for i in range(len(idx2word_java)):
    java_word2idx[idx2word_java[i]] = i
for i in range(len(idx2word_Cpp)):
    Cpp_word2idx[idx2word_Cpp[i]] = i

with open('daniel_full_set.jsonl', 'r') as f:
    with open('indexed_trees_labeled_Cpp.jsonl', 'w') as c, open('indexed_trees_labeled_Java.jsonl', 'w') as j:
        line_count = 0
        for line in f:
            d = json.loads(line)
            label = d['hired']
            code_list = d['solutions']
            Cpp_list = []; Java_list = []
            for code in code_list:
                count = 0
                if len(code) < 25:
                    continue
                try:
                    raw_tree = util.parse_tree_Java(code)
                    indexed_tree = util.index_tree_Java(raw_tree, java_word2idx)
                    language = 'Java'
                except javalang_master.javalang.tokenizer.LexerError:
                    code_stripped = ''
                    for l in code.splitlines():
                        if 'include' in l or 'import' in l:
                            continue
                        code_stripped = '\n'.join([code_stripped, l])
                    code_stripped = code_stripped.strip()
                    raw_tree = util.parse_tree_Cpp(code_stripped).cursor
                    indexed_tree = util.index_tree_Cpp(raw_tree, Cpp_word2idx)
                    language = 'C++'
                except:
                    continue
                r = []; util.serialize(indexed_tree, r)
                if len(r) >= 10:
                    if language == 'Java':
                        Java_list.append(r)
                    elif language == 'C++':
                        Cpp_list.append(r)
            if len(Cpp_list) > 0:
                c.write(json.dumps({'hired': label, 'solutions': Cpp_list}) + '\n')
            if len(Java_list) > 0:
                j.write(json.dumps({'hired': label, 'solutions': Java_list}) + '\n')
            line_count += 1
            if line_count % 500 == 0:
                print (line_count)

print ('Done writing data')