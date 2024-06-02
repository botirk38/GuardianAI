pub mod analyzer {
    tonic::include_proto!("analyzer");
}

use analyzer::analyzer_client::AnalyzerClient;
use analyzer::AnalyzeRequest;
use crate::engine::CodeFeatures;
use std::error::Error;

pub async fn detect_vulnerabilities(code_features: CodeFeatures) -> Result<String, Box<dyn Error>> {
    let mut client = AnalyzerClient::connect("http://[::1]:50051").await?;

    let request = tonic::Request::new(AnalyzeRequest {
        features_json: serde_json::to_string(&code_features)?,
    });

    let response = client.analyze_contract(request).await?;

    Ok(response.into_inner().vulnerabilities_json)
}
