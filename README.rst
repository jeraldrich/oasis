Oasis Gov Bad List Scraper
--------

Just a fun little project to create a scraper using flask, celery, and redis. Not very efficient, but shows a full stack from js call to http server to background poll processing of search queries.

To extract package::
    - (On Linux / OSX) tar xvf oasis.tgz
    - (On Windows) Double click on oasis.tgz
    - the oasis directory will then be created

To install:
    - install python-virtualenv (os package)
    - install uwsgi (os package)
    - install uwsgi-plugin-python (os package)
    - sh install.sh
    - sh install-redis.sh

To run::
    - sh run.sh
    - sh run-redis.sh
    - sh run-celery.sh
