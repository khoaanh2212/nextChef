=========
Next Chef
=========

Prerequisites
-------------

* docker-engine >= 1.10 (add user to docker group: `sudo gpasswd -a ${USER} docker`)

* docker-compose >= 1.6


Run tests as in C.I.
--------------------
```
    $ make docker-image && make docker-test // unit and integration tests
    $ make docker-image && make docker-ft // system tests
```
Run local demo server
---------------------
```
    $ ./start_qa.sh
```
    
Go to: http://localhost:8001

Clean all data
--------------
```
    REGISTRY=docker.apiumtech.io TAG=latest docker-compose -p nextchefqa -f compose/base.yml -f compose/qa.yml down -v
```
Import test data
----------------
```
    REGISTRY=docker.apiumtech.io TAG=latest docker-compose -p nextchefqa -f compose/base.yml -f compose/qa.yml -f compose/tasks.yml run importtestdata
```
Then restart the containers again.


=======================
Development environment
=======================


Prerequisites
-------------

* Ubuntu 14.04 desktop (you could use another OS at your own risk)

* Libraries
```
    sudo apt-get install libxml2-dev libxslt1-dev python-dev libmysqlclient-dev libpython2.7-dev libssl-dev
```

* Python 2.7.11
    Follow: http://mbless.de/blog/2016/01/09/upgrade-to-python-2711-on-ubuntu-1404-lts.html

* pip
```
    $ easy_install pip
```

* virtualenv:
```
    $ pip install virtualenv
```
    
* Add following line to /etc/hosts:
```
    127.0.0.1	nextchef.db nextchef.redis nextchef.elasticsearch
```

Project setup
-------------

Start external services (mysql, redis, elasticsearch, less watcher):
```
        $ ./start_dev_services.sh
```
     
Create a virtual environnment for python ():
```
        $ virtualenv .python-env // OK
        // not just '.env' because .env is used by docker-compose
```

Activate your environment:
```
        $ source .python-env/bin/activate
```

Install project requirements (asuming your environment is active):
```
        $ pip install -r ./requirements/local.txt
        $ pip install -r ./requirements/test.txt
```

Run all tests
```
        $ ./manage.py test --settings=backend.settings.test
        $ ./manage.py test unit_tests
```
        
Run server:
```
        $ python backend/runserver.py
```

Run server faster (no db warmup, do this only after your db is already up and migrated)
```
        $ python backend/run_develop_server.py
```

Manage.py tasks (at /path/to/backend_project/backend):

    Sync db:
```    
        $ ./manage.py syncdb
```

    Migration:
```
    
        $ ./manage.py migrate
```

    Elastic search indexes:
```    
        $ ./manage.py es_reindex_recipes
```

    Creating superadmin user:
```
        $ ./manage.py createsuperuser
```


South tips

    Create initial migration for an application:
```        
        $ ./manage.py schemamigration accounts --initial
```

    Create migration after changing a model:
```
        $ ./manage.py schemamigration accounts --auto
```

    Apply migration:
```
        $ ./manage.py migrate accounts
```

    See migrations:
```
        $ ./manage.py migrate --list
```

    Loading fixture data
```
        $ ./manage.py loaddata brands
```


===================
Configuring Pycharm
===================

-------------------------
``1. PREPARATION``
-------------------------

Install it from: https://www.jetbrains.com/pycharm/

Make sure your development environment is ready and all needed services are running.

You should run PyCharm with injected environment variables in the command line:

```
    $ TEST_DATA=true DJANGO_SETTINGS_MODULE=backend.settings.test /path/to/pycharm/bin/pycharm.sh &
```

After this, you will need to configure a remote interpreter:

In PyCharm, go to File > Settings > Project : backend > Project Interpreter

There, select the Virtual Env at backend/.python-env

Then, In Project Structure. You need to mark the folder backend at /your/path/to/backend_project/backend as "Source".

------------------------------------
``2. RUNNING THE SERVER IN THE IDE``
------------------------------------

Go to Run > Edit Configurations

Add New Configuration > Python

In Script: /path/to/backend_project/backend/runserver.py

After migrations are run, server will be running.

You must also be able to run the debugger using the same configuration from PyCharm.

--------------------------------------
``3. RUNNING PYTHON TESTS IN THE IDE``
--------------------------------------

Add New Configuration > Python Tests > Unittests

Mark the option "All in Folder".
    
In Folder: /path/to/backend_project/backend

After that, you should be able to run and debug this configuration from pycharm.

You can reduce the scope of tests by modifying the folder. For example:

    - Unit Tests path: /path/to/backend_project/backend/unit_tests
    - New Integration Tests path: /path/to/backend_project/backend/integration_tests
    - Legacy Chef Tests path: /path/to/backend_project/backend/chefs/tests
    
--------------------------------------
``4. RUNNING FRONTEND TESTS IN THE IDE``
----------------------------------------

Install node.js

Install dependencies:

```
    $ npm install
```

Install Karma plugin on PyCharm.

Add New Configuration > Karma
    
In Configuration file: /path/to/backend_project/frontend_tests/karma.conf.js

Environment Variables you might want to modify
----------------------------------------------

1. TEST_DATA:

    For having data in your development environment, please set the environment variable TEST_DATA to "true" before running the app.

2. INIT_STRIPE_PLANS:

    If you want to initialize the EDAMAM remote backend and update your database with the result, you need to set the environment variable INIT_STRIPE_PLANS to "true" before running the app (not done by default in any start_*.sh script). You should not need to do this anymore unless any change on the payment implementation is performed.


