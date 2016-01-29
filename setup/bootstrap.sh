#!/bin/bash

export DOTFILES=$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )

echo "Add to bash profile: source $DOTFILES/etc/bash/config"
if [ "$(uname)" == "Darwin" ]; then
    echo "source $DOTFILES/etc/bash/config" >> ~/.bash_profile
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
	echo "source $DOTFILES/etc/bash/config" >> ~/.bash_profile
else
    echo "source $DOTFILES/etc/bash/config" >> ~/.bashrc
fi
echo "Link git configuration"
ln -s $DOTFILES/etc/git/config ~/.gitconfig
