use quote::ToTokens;
use serde::{Deserialize, Serialize};
use syn::{parse_file, Item};

#[derive(Serialize, Deserialize, Debug)]
pub struct FunctionInfo {
    pub name: String,
    pub visibility: String,
    pub attributes: usize,
    pub params: Vec<String>,
    pub expressions: Vec<String>, // Store expressions as strings
}

#[derive(Serialize, Deserialize, Debug)]
pub struct StructInfo {
    pub name: String,
    pub fields: usize,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct EnumInfo {
    pub name: String,
    pub variants: Vec<String>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ModInfo {
    pub name: String,
    pub item_count: usize,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ConstInfo {
    pub name: String,
    pub value: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct StaticInfo {
    pub name: String,
    pub mutable: bool,
    pub value: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ImplInfo {
    pub name: String,
    pub methods: Vec<FunctionInfo>,
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "type", content = "data")]
pub enum AstItem {
    Function(FunctionInfo),
    Struct(StructInfo),
    Enum(EnumInfo),
    Mod(ModInfo),
    Const(ConstInfo),
    Static(StaticInfo),
    Other(String),
    Impl(ImplInfo),
}

pub fn parse_code_ast(code: &str) -> Result<Vec<AstItem>, Box<dyn std::error::Error>> {
    let ast = parse_file(code).map_err(|e| format!("Failed to parse code: {}", e))?;
    let mut ast_items = Vec::new();

    for item in ast.items {
        match item {
            Item::Fn(item_fn) => {
                let params = item_fn
                    .sig
                    .inputs
                    .iter()
                    .map(|arg| arg.to_token_stream().to_string())
                    .collect();
                let expressions = extract_expressions(&item_fn.block);

                ast_items.push(AstItem::Function(FunctionInfo {
                    name: item_fn.sig.ident.to_string(),
                    visibility: visibility_to_string(&item_fn.vis),
                    attributes: item_fn.attrs.len(),
                    params,
                    expressions,
                }));
            }

            Item::Impl(item_impl) => {
                let methods = item_impl
                    .items
                    .iter()
                    .filter_map(|item| {
                        if let syn::ImplItem::Method(method) = item {
                            let params = method
                                .sig
                                .inputs
                                .iter()
                                .map(|arg| arg.to_token_stream().to_string())
                                .collect();
                            let expressions = extract_expressions(&method.block);

                            Some(FunctionInfo {
                                name: method.sig.ident.to_string(),
                                visibility: visibility_to_string(&method.vis),
                                attributes: method.attrs.len(),
                                params,
                                expressions,
                            })
                        } else {
                            None
                        }


                    })
                    .collect();

                ast_items.push(AstItem::Impl(ImplInfo {
                    name: item_impl
                        .trait_
                        .as_ref()
                        .map(|t| t.1.to_token_stream().to_string())
                        .unwrap_or_else(|| "impl".to_string()),
                    methods,
                }));
            }

            Item::Struct(item_struct) => {
                ast_items.push(AstItem::Struct(StructInfo {
                    name: item_struct.ident.to_string(),
                    fields: item_struct.fields.iter().count(),
                }));
            }
            Item::Enum(item_enum) => {
                ast_items.push(AstItem::Enum(EnumInfo {
                    name: item_enum.ident.to_string(),
                    variants: item_enum
                        .variants
                        .iter()
                        .map(|v| v.ident.to_string())
                        .collect(),
                }));
            }
            Item::Mod(item_mod) => {
                if let Some((_, items)) = &item_mod.content {
                    ast_items.push(AstItem::Mod(ModInfo {
                        name: item_mod.ident.to_string(),
                        item_count: items.len(),
                    }));
                } else {
                    ast_items.push(AstItem::Mod(ModInfo {
                        name: item_mod.ident.to_string(),
                        item_count: 0,
                    }));
                }
            }
            Item::Const(item_const) => {
                ast_items.push(AstItem::Const(ConstInfo {
                    name: item_const.ident.to_string(),
                    value: item_const.expr.to_token_stream().to_string(),
                }));
            }
            Item::Static(item_static) => {
                ast_items.push(AstItem::Static(StaticInfo {
                    name: item_static.ident.to_string(),
                    mutable: item_static.mutability.is_some(),
                    value: item_static.expr.to_token_stream().to_string(),
                }));
            }

            _ => {
                ast_items.push(AstItem::Other(format!("{:?}", item_to_string(&item))));
            }
        }
    }

    Ok(ast_items)
}

fn visibility_to_string(vis: &syn::Visibility) -> String {
    match vis {
        syn::Visibility::Public(_) => "public".to_string(),
        syn::Visibility::Crate(_) => "crate".to_string(),
        syn::Visibility::Restricted(_) => "restricted".to_string(),
        syn::Visibility::Inherited => "inherited".to_string(),
    }
}

fn item_to_string(item: &syn::Item) -> String {
    match item {
        Item::Const(_) => "const".to_string(),
        Item::ExternCrate(_) => "extern crate".to_string(),
        Item::ForeignMod(_) => "foreign mod".to_string(),
        Item::Impl(_) => "impl".to_string(),
        Item::Macro(_) => "macro".to_string(),
        Item::Macro2(_) => "macro2".to_string(),
        Item::Mod(_) => "mod".to_string(),
        Item::Static(_) => "static".to_string(),
        Item::Trait(_) => "trait".to_string(),
        Item::TraitAlias(_) => "trait alias".to_string(),
        Item::Type(_) => "type".to_string(),
        Item::Union(_) => "union".to_string(),
        Item::Use(_) => "use".to_string(),
        _ => "other".to_string(),
    }
}

fn extract_expressions(block: &syn::Block) -> Vec<String> {
    block
        .stmts
        .iter()
        .map(|stmt| stmt.to_token_stream().to_string())
        .collect()
}
