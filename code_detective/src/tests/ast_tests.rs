 use crate::engine::ast::{parse_code_ast, AstItem};

  #[test]
    fn test_parse_function() {
        let code = r#"
        pub fn test_func(a: i32, b: String) -> i32 {
            let c = a + 1;
            c
        }
        "#;

        let result = parse_code_ast(code).unwrap();
        assert_eq!(result.len(), 1);

        if let AstItem::Function(func) = &result[0] {
            assert_eq!(func.name, "test_func");
            assert_eq!(func.visibility, "public");
            assert_eq!(func.attributes, 0);
            assert_eq!(func.params, vec!["a : i32", "b : String"]);
            assert_eq!(func.expressions, vec!["let c = a + 1 ;", "c"]);
        } else {
            panic!("Expected function item");
        }
    }

    #[test]
    fn test_parse_struct() {
        let code = r#"
        pub struct TestStruct {
            a: i32,
            b: String,
        }
        "#;

        let result = parse_code_ast(code).unwrap();
        assert_eq!(result.len(), 1);

        if let AstItem::Struct(strct) = &result[0] {
            assert_eq!(strct.name, "TestStruct");
            assert_eq!(strct.fields, 2);
        } else {
            panic!("Expected struct item");
        }
    }

    #[test]
    fn test_parse_enum() {
        let code = r#"
        pub enum TestEnum {
            Variant1,
            Variant2(i32),
            Variant3 { a: String },
        }
        "#;

        let result = parse_code_ast(code).unwrap();
        assert_eq!(result.len(), 1);

        if let AstItem::Enum(enm) = &result[0] {
            assert_eq!(enm.name, "TestEnum");
            assert_eq!(enm.variants, vec!["Variant1", "Variant2", "Variant3"]);
        } else {
            panic!("Expected enum item");
        }
    }

    #[test]
    fn test_parse_mod() {
        let code = r#"
        pub mod test_mod {
            pub fn test_func() {}
            pub struct TestStruct;
        }
        "#;

        let result = parse_code_ast(code).unwrap();
        assert_eq!(result.len(), 1);

        if let AstItem::Mod(md) = &result[0] {
            assert_eq!(md.name, "test_mod");
            assert_eq!(md.item_count, 2);
        } else {
            panic!("Expected mod item");
        }
    }

    #[test]
    fn test_parse_const() {
        let code = r#"
        pub const TEST_CONST: i32 = 42;
        "#;

        let result = parse_code_ast(code).unwrap();
        assert_eq!(result.len(), 1);

        if let AstItem::Const(cnst) = &result[0] {
            assert_eq!(cnst.name, "TEST_CONST");
            assert_eq!(cnst.value, "42");
        } else {
            panic!("Expected const item");
        }
    }

    #[test]
    fn test_parse_static() {
        let code = r#"
        pub static mut TEST_STATIC: i32 = 42;
        "#;

        let result = parse_code_ast(code).unwrap();
        assert_eq!(result.len(), 1);

        if let AstItem::Static(stc) = &result[0] {
            assert_eq!(stc.name, "TEST_STATIC");
            assert_eq!(stc.mutable, true);
            assert_eq!(stc.value, "42");
        } else {
            panic!("Expected static item");
        }
    }

    #[test]
    fn test_parse_impl() {
        let code = r#"
        pub struct TestStruct;

        impl TestStruct {
            pub fn new() -> Self {
                TestStruct
            }
            fn private_method(&self) {}
        }
        "#;

        let result = parse_code_ast(code).unwrap();
        assert_eq!(result.len(), 2); // One for struct, one for impl

        if let AstItem::Impl(imp) = &result[1] {
            assert_eq!(imp.name, "impl");
            assert_eq!(imp.methods.len(), 2);

            let method = &imp.methods[0];
            assert_eq!(method.name, "new");
            assert_eq!(method.visibility, "public");
            assert_eq!(method.attributes, 0);
            assert_eq!(method.params, vec![] as Vec<String>);
            assert_eq!(method.expressions, vec!["TestStruct"]);

            let private_method = &imp.methods[1];
            assert_eq!(private_method.name, "private_method");
            assert_eq!(private_method.visibility, "inherited");
            assert_eq!(private_method.params, vec!["& self"]);
            assert_eq!(private_method.expressions.len(), 0);
        } else {
            panic!("Expected impl item");
        }
    }

