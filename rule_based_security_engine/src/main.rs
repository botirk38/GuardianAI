#[macro_use]
extern crate diesel;

use actix_web::{web, App, HttpResponse, HttpServer, Responder};

mod api;  
mod models;
mod schema;
mod engine;

async fn index() -> impl Responder {
    HttpResponse::Ok().body("Solana Security Analyzer Running")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();

    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(index))
            .configure(api::init_routes) 
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}

