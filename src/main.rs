use env_logger;
use std::env;


mod types;
mod service;

fn main() {

    env::set_var("RUST_LOG", "info");
    env_logger::init();

    service::read_zip("")
}
