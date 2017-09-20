#! /bin/sh
pip install --extra-index-url=$PIP_EXTRA_INDEX_URL -r ./requirements/test.txt
pip install --extra-index-url=$PIP_EXTRA_INDEX_URL -e .[peewee,redis,queues]
"$@"
