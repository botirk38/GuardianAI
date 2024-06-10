pub mod analyzer {
    tonic::include_proto!("analyzer");
}

use crate::engine::CodeFeatures;
use analyzer::analyzer_client::AnalyzerClient;
use analyzer::AnalyzeRequest;
use std::env;
use std::error::Error;

pub async fn detect_vulnerabilities(code_features: CodeFeatures) -> Result<String, Box<dyn Error>> {
    let grpc_server_url =
        env::var("GRPC_SERVER_URL").unwrap_or_else(|_| "http://[::1]:50051".to_string());

    println!("Server URL: {:?} ", grpc_server_url);

    let mut client = AnalyzerClient::connect(grpc_server_url).await?;

    let request = tonic::Request::new(AnalyzeRequest {
        features_json: serde_json::to_string(&code_features)?,
    });

    match client.analyze_contract(request).await {
        Ok(response) => Ok(response.into_inner().vulnerabilities_json),
        Err(e) => Err(Box::new(e)),
    }
}

