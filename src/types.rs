use serde::Deserialize;

use std::fs::File;
use std::io::BufReader;
use std::path::Path;
use std::error::Error;


#[derive(Deserialize, Debug)]
pub struct User {
    pub id: Option<f64>,
    pub screen_name: Option<String>,
}

#[derive(Deserialize, Debug)]
pub struct RetweetedStatus {
    pub id_str: Option<String>,
    pub text: Option<String>,
    pub user: Option<User>
}

#[derive(Deserialize, Debug)]
pub struct Entities {
    pub user_mentions: Option<Vec<UserMention>>
}

#[derive(Deserialize, Debug)]
pub struct UserMention {
    pub screen_name: Option<String>
}

#[derive(Deserialize, Debug)]
pub struct TimeLine {

    pub created_at: Option<String>,
    pub id: Option<f64>,
    pub id_str: Option<String>,
    pub text: Option<String>,
    pub truncated: Option<bool>,
    pub source: Option<String>,
    pub user: Option<User>,
    pub retweeted_status: Option<RetweetedStatus>,
    pub entities: Option<Entities>,
    pub in_reply_to_user_id_str: Option<String>
}


pub fn get_json_data<P: AsRef<Path>>(path: P) -> Result<Vec<TimeLine>, Box<dyn Error>>{
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let t: Vec<TimeLine> = serde_json::from_reader(reader)?;

    Ok(t)
}



#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn is_get_json_data() {
        println!("Twitterのタイムライン情報の型変換が通ることを確認");

        let path = "./src/assets/test_timeline_data.json";
        get_json_data(path).unwrap();

        assert_eq!(true, true);
    }
}

