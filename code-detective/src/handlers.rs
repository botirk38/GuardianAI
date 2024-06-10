use crate::{engine::analyze_code, grpc_client::detect_vulnerabilities};
use actix_web::{web, HttpResponse, Responder};
use serde::Deserialize;
use serde_json::Value;

#[derive(Deserialize)]
pub struct SmartContract {
    code: String,
}

pub async fn analyze_code_handler(smart_contract: web::Json<SmartContract>) -> impl Responder {
    let code_features = analyze_code(&smart_contract.code);
    println!("Code features {:?}", code_features);

    match detect_vulnerabilities(code_features).await {
        Ok(vulnerabilities) => {
            // Parse the JSON string returned from the gRPC client
            match serde_json::from_str::<Value>(&vulnerabilities) {
                Ok(json_value) => HttpResponse::Ok().json(json_value),
                Err(e) => {
                    HttpResponse::InternalServerError().body(format!("Failed to parse JSON: {}", e))
                }
            }
        }
        Err(e) => HttpResponse::InternalServerError().body(format!("gRPC request failed: {}", e)),
    }
}

