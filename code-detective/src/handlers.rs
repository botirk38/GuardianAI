use crate::{
    engine::{analyze_code, CodeFeatures},
    producer::send_code_for_analysis,
};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct SmartContract {
    code: String,
    request_id: String,
}

#[derive(Serialize)]
pub struct AnalysisRequest {
    request_id: String,
    code_features: CodeFeatures,
}

pub async fn analyze_code_handler(smart_contract: web::Json<SmartContract>) -> impl Responder {
    let code_features = analyze_code(&smart_contract.code);
    println!("Code features {:?}", code_features);

    let request_id = smart_contract.request_id.clone();

    let analysis_request = AnalysisRequest {
        request_id,
        code_features,
    };

    match send_code_for_analysis(analysis_request).await {
        Ok(_) => HttpResponse::Ok().body("Request sent for analysis"),
        Err(e) => {
            HttpResponse::InternalServerError().body(format!("Failed to send request: {}", e))
        }
    }
}

