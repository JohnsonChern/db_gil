# settings for Postgres

dbuser          = "root"
dbname          = "privacy_server"
dbuserpassword  = "johnson"

"""

To create a user and a database:
1. run "sudo su - postgres" in terminal, then input the password.
2. run "createuser -d your_username"
3. exit
4. run "createdb your_dbname"
5. after  create a user and database, run setup_db.py

"""