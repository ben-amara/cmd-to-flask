#!/bin/bash

gunicorn --bind 127.0.0.1:4000  --workers=2 wsgi:app &
