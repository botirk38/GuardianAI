use actix_web::{web, HttpResponse, Responder};
use serde::Deserialize;
use crate::engine::ast;

#[derive(Debug, Deserialize)]
pub struct SmartContract {
    pub code: String,
}

pub async fn index() -> impl Responder {
    HttpResponse::Ok().body("Service is running")
}

pub async fn analyze_contract(body: web::Json<SmartContract>) -> impl Responder {
    let code = &body.code;

    if code.is_empty() {
        return HttpResponse::BadRequest().body("Empty code");
    }

    let ast = match ast::parse_code_ast(code) {
        Ok(ast) => format!("{:?}", ast),
        Err(e) => format!("Error parsing code: {}", e),
    };

    let ast_json = serde_json::to_string(&ast).unwrap();

    println!("AST: {}", ast_json);

    HttpResponse::Ok().json(ast_json)


}
