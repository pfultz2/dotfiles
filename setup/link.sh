#!/bin/bash

set -x

export DOTFILES=$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )

echo "Link git configuration"
ln -s $DOTFILES/etc/git/config ~/.gitconfig

echo "Link screenrc"
ln -s $DOTFILES/etc/.screenrc ~/.screenrc

echo "Link tmux configuration"
ln -s $DOTFILES/etc/.tmux.conf ~/.tmux.conf

echo "Link nanorc"
ln -s $DOTFILES/etc/.nanorc ~/.nanorc

if [ "$(uname)" == "Darwin" ]; then
    export SUBLIME_PACKAGE_DIR=$HOME/Library/Application\ Support/Sublime\ Text\ 3/Packages
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    export SUBLIME_PACKAGE_DIR="$HOME/AppData/Roaming/Sublime Text 3/Packages"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    export SUBLIME_PACKAGE_DIR="$HOME/AppData/Roaming/Sublime Text 3/Packages"
else
    export SUBLIME_PACKAGE_DIR=$HOME/.config/sublime-text-3/Packages
fi
echo "Link sublime configuration"
mkdir -p "$SUBLIME_PACKAGE_DIR"
ln -s "$DOTFILES/etc/sublime" "$SUBLIME_PACKAGE_DIR/User"
if [ "$(uname)" == "Darwin" ]; then
    echo "Link key bindings"
    mkdir -p ~/Library/KeyBindings
    ln -s "$DOTFILES/etc/mac/DefaultKeyBinding.dict" ~/Library/KeyBindings/DefaultKeyBinding.dict
fi
