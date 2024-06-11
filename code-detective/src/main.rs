mod engine;
mod grpc_client;
mod handlers;
mod producer;
mod tests;

use actix_web::{web, App, HttpServer};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new().route(
            "/analyze_code",
            web::post().to(handlers::analyze_code_handler),
        )
    })
    .bind("0.0.0.0:8081")?
    .run()
    .await
}
