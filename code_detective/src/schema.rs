
diesel::table! {
    rules (id) {
        id -> Int4,
        name -> Varchar,
        description -> Text,
    }
}

diesel::table! {
    vulnerabilities (id) {
        id -> Int4,
        rule_id -> Int4,
        name -> Varchar,
        description -> Text,
        severity -> Varchar,
    }
}

diesel::joinable!(vulnerabilities -> rules (rule_id));

diesel::allow_tables_to_appear_in_same_query!(
    rules,
    vulnerabilities,
);
