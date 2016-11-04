#!/bin/bash

export DOTFILES=$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )

echo "Add to bash profile: source $DOTFILES/etc/bash/config"
if [ "$(uname)" == "Darwin" ]; then
    echo "source $DOTFILES/etc/bash/config" >> ~/.bash_profile
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "source $DOTFILES/etc/bash/config" >> ~/.bash_profile
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "source $DOTFILES/etc/bash/config" >> ~/.bash_profile
else
    echo "source $DOTFILES/etc/bash/config" >> ~/.bashrc
fi
echo "Link git configuration"
ln -s $DOTFILES/etc/git/config ~/.gitconfig

if [ "$(uname)" == "Darwin" ]; then
    export SUBLIME_PACKAGE_DIR=$HOME/Library/Application\ Support/Sublime\ Text\ 3/Packages
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    export SUBLIME_PACKAGE_DIR="/c/Users/$USER/AppData/Roaming/Sublime Text 3/Packages"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    export SUBLIME_PACKAGE_DIR="/c/Users/$USER/AppData/Roaming/Sublime Text 3/Packages"
else
    export SUBLIME_PACKAGE_DIR=$HOME/.config/sublime-text-3/Packages
fi
echo "Link sublime configuration"
mkdir -p $SUBLIME_PACKAGE_DIR
ln -s $DOTFILES/etc/sublime $SUBLIME_PACKAGE_DIR/User
