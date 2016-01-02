# Database of Privacy Policy

## Setting up database:

1. read and modify config_db.py

2. run setup_db.py to set up a table named "privacy_server"


## About the database:

The table in your database is with relation: 

( *patient_id, policy, last_modified* ):

*   *patient_id*:
     
     the unique identifier, long type by default

*   *policy*:

     patient's privacy policy, json type by default
     
*   *last_modified*:

     last_time that the policy is modified 