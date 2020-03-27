#!/bin/bash

source $DOTFILES/bin/remote-setup.sh

CMD="cd $DEST_DIR; $*"
ssh -tt $HOST bash -l << EOF
cd $DEST_DIR
$*
EOF
