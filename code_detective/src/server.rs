use crate::engine::analyze_code;
use analyzer::analyzer_server::{Analyzer, AnalyzerServer};
use analyzer::{AnalyzeRequest, AnalyzeResponse};
use tonic::{transport::Server, Request, Response, Status};

#[macro_use]
extern crate diesel;

mod engine;
mod models;
mod schema;
mod tests;

pub mod analyzer {
    tonic::include_proto!("analyzer");
}

#[derive(Default)]
pub struct MyAnalyzer {}

#[tonic::async_trait]
impl Analyzer for MyAnalyzer {
    async fn analyze_contract(
        &self,
        request: Request<AnalyzeRequest>,
    ) -> Result<Response<AnalyzeResponse>, Status> {
        let code = &request.into_inner().code;

        if code.is_empty() {
            return Err(Status::invalid_argument("Empty code"));
        }

        // Simulate the analysis process
        let features = analyze_code(code);
        let features_json = serde_json::to_string(&features).unwrap();

        let response = AnalyzeResponse { features_json };
        Ok(Response::new(response))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50051".parse()?;
    let analyzer = MyAnalyzer::default();

    Server::builder()
        .add_service(AnalyzerServer::new(analyzer))
        .serve(addr)
        .await?;

    Ok(())
}

