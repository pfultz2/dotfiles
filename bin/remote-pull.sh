#!/bin/sh

source ~/bin/remote-setup.sh

rsync --verbose --recursive --times --compress --progress\
    --exclude ".hg" \
    --exclude ".git" \
    --exclude "*build" \
    --exclude "build*" \
        $HOST:$DEST_DIR/ $CURR_DIR