use diesel::pg::PgConnection;
use diesel::RunQueryDsl;
use serde::{Deserialize, Serialize};

use crate::schema::rules as rules_dsl;

#[derive(Queryable, Serialize, Deserialize)]
#[diesel(table_name = "rules")]
pub struct Rule {
    pub id: i32,
    pub name: String,
    pub description: String,
}

impl Rule {
    pub fn fetch_all(conn: &PgConnection) -> Result<Vec<Self>, diesel::result::Error> {
        use rules_dsl::dsl::*;

        rules.load::<Rule>(conn)
    }
}

