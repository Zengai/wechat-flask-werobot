#!/bin/sh
gunicorn --bind="0.0.0.0:80" --workers=4 --worker-class gevent run:app