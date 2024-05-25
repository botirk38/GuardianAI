
mod handlers;

use actix_web::web;

pub fn init_routes(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/code-detective")
            .route("/", web::get().to(handlers::index))
            .route("/analyze", web::post().to(handlers::analyze_contract))
    );
}

