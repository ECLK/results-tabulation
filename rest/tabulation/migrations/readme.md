# Database Migrations

All the alterations of the database is done by the migration plugin called `alembic` supports for `sql-alchemy`.
Whenever any changes have been made to `sql-alchemy` modules in [orm](./orm), it has to be added to migration files
as a new revision by running a migration script.

**Make a revision**

If there are changes identified, a revision file is created at migrations/versions with a hash.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db migrate`

Also, please pay attention to the database alteration changes auto generated in the revision file and make necessary 
changes in it as required.

1. If there's a new required column added to an existing entity, as update script also has to be included to fill the column for existing records.

**Upgrade database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py db upgrade`

This script will check whether the database has the latest revision and if not, update the database to the latest.

**Merge heads**

When the commits are merged and if there are migration files merged, it's required to do this.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db merge heads`

**Drop database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py drop_database`