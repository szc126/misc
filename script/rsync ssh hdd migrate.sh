#!/usr/bin/env bash

rsync --verbose --archive --progress --delete -e "ssh" /media/e-docs/ "$1":/media/e-docs/
