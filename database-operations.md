# Database Operations

**Initialize migration**

This is a one time thing which is required only at the project beginning. The information is only for knowledge.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db init`

**Make a revision**

If there are changes identified, a revision file is created at migrations/versions with a hash.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db migrate`

**Upgrade database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py db upgrade`

**Merge heads**

When the commits are merged and if there are migration files merged, it's required to do this.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db merge heads`

**Drop database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py drop_database`
