use rdkafka::config::ClientConfig;
use rdkafka::producer::{FutureProducer, FutureRecord};
use std::time::Duration;
use std::boxed::Box;
use crate::handlers::AnalysisRequest;


pub async fn send_code_for_analysis(analysis_request: AnalysisRequest) -> Result<(), Box<dyn std::error::Error>> {
    let producer: FutureProducer = ClientConfig::new()
        .set("bootstrap.servers", "localhost:9092")
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



