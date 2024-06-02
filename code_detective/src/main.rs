
mod engine;
mod tests;
mod handlers;
mod grpc_client;

use actix_web::{web, App, HttpServer};


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/analyze_code", web::post().to(handlers::analyze_code_handler))
    })
    .bind("127.0.0.1:8081")?
    .run()
    .await
}
