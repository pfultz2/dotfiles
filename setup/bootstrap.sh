#!/bin/bash

set -x

export DOTFILES=$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )

echo "Add to bash profile: source $DOTFILES/etc/bash/config"
if [ "$(uname)" == "Darwin" ]; then
    echo "source $DOTFILES/etc/bash/config" >> ~/.bash_profile
    echo "source $DOTFILES/etc/bash/config" >> ~/.zshrc
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "source $DOTFILES/etc/bash/config" >> ~/.bash_profile
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "source $DOTFILES/etc/bash/config" >> ~/.bash_profile
else
    echo "source $DOTFILES/etc/bash/config" >> ~/.bashrc
fi

# TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# oh-my-zsh
git clone https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh

git clone https://github.com/zsh-users/zsh-autosuggestions.git ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting

# Facebook path picker
git clone https://github.com/facebook/PathPicker.git $DOTFILES/pathpicker

# Link files
$DOTFILES/setup/link.sh
