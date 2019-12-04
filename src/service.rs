use std::error::Error;
use std::collections::HashMap;
use std::{fs, io, mem};
use std::io::{Read, BufReader};
use std::fs::File;
use std::ffi::OsStr;
use std::path::Path;

use log::{info, trace, warn};

use crate::types::{get_json_data, TimeLine};
use std::borrow::Borrow;


mod csv_setting {
    use serde::Serialize;

    #[derive(Debug,Serialize)]
    pub struct Timeline {
        pub text: String
    }
}


pub fn read_zip<P: AsRef<Path>>(path: P) {
    info!("ZIPファイルの読み込みを開始します。");

    let args: Vec<_> = std::env::args().collect();

    let fname = std::path::Path::new(path.as_ref());
    let file = fs::File::open(&fname).unwrap();
    let mut archive = zip::ZipArchive::new(file).unwrap();
    let mut count: usize = 0;
    let mut wtr = csv::Writer::from_path("./asd.csv").unwrap();

    for i in 0..archive.len() {
        let mut file = archive.by_index(i).unwrap();

        if file.is_file() {
            let timeline_list: Vec<TimeLine> = serde_json::from_reader(BufReader::new(file)).unwrap();

            for timeline in &timeline_list {
                wtr.serialize(csv_setting::Timeline {
                    text: String::from(timeline.text.as_ref().unwrap())
                });
            }

            count += timeline_list.len();
            if i % 100 == 0 {
                info!("全ファイル: {} 現在のファイル数: {}, 処理済み: {}", archive.len(), i, count);
            }
        }
    }

    wtr.flush();

    info!("ZIPファイルの読み込み処理が完了しました。");
}

pub struct Service {}

impl Service {
    fn dump1() -> Result<i8, Box<dyn Error>>{
//        let path = "./src/assets/test_timeline_data.json";
//        let timelineList: Vec<TimeLine> = get_json_data(path)?;
//
//        let mut scores = HashMap::new();
//
//        for timeline in &timelineList {
//            print!("{:?}", timeline.text.as_ref());
//            scores.insert("a", timeline.id_str.as_ref());
//        }

        Ok(1)
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_read_zip() {
        read_zip()
    }

//    mod Service {
//        #[test]
//        fn test_dump1() {
//            Service::dump1().unwrap();
//        }
//    }
}


