#!/bin/bash

export DOTFILES=$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )

if [ "$(uname)" == "Darwin" ]; then
    echo "source $DOTFILES/etc/bash/config" >> .bash_profile
else
    echo "source $DOTFILES/etc/bash/config" >> .bashrc
fi

ln -s $DOTFILES/etc/git/config .gitconfig
