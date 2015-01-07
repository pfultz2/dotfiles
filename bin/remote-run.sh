#!/bin/sh

source ~/bin/remote-setup.sh

ssh $HOST "cd $DEST_DIR && $*"
