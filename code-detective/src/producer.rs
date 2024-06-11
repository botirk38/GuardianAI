use dotenv::dotenv;
use std::env;
use rdkafka::config::ClientConfig;
use rdkafka::producer::{FutureProducer, FutureRecord};
use std::time::Duration;
use std::boxed::Box;
use crate::handlers::AnalysisRequest;

pub async fn send_code_for_analysis(analysis_request: AnalysisRequest) -> Result<(), Box<dyn std::error::Error>> {
    dotenv().ok();

    let kafka_bootstrap_servers = env::var("KAFKA_ADDR")
        .unwrap_or_else(|_| "localhost:9092".to_string());

    let producer: FutureProducer = ClientConfig::new()
        .set("bootstrap.servers", &kafka_bootstrap_servers)
        .create()
        .expect("Producer creation error");

    let payload = serde_json::to_string(&analysis_request)?;

    producer.send(
        FutureRecord::to("code-analysis-requests")
            .payload(&payload)
            .key("request"),
        Duration::from_secs(0),
    ).await.map_err(|(e, _)| Box::new(e) as Box<dyn std::error::Error>)?;

    Ok(())
}

