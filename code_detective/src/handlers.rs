use crate::{engine::analyze_code, grpc_client::detect_vulnerabilities};
use actix_web::{web, HttpResponse, Responder};
use serde::Deserialize;

#[derive(Deserialize)]
pub struct SmartContract {
    code: String,
}

pub async fn analyze_code_handler(smart_contract: web::Json<SmartContract>) -> impl Responder {
    let code_features = analyze_code(&smart_contract.code);
    println!("Code features {:?}", code_features);

    match detect_vulnerabilities(code_features).await {
        Ok(vulnerabilities) => HttpResponse::Ok().json(vulnerabilities),
        Err(e) => HttpResponse::InternalServerError().body(format!("gRPC request failed: {}", e)),
    }
}
