#!/bin/sh
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
echo "alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'" >> $HOME/.bashrc
echo ".cfg" >> .gitignore
git clone --bare git@github.com:NevilleJS/dotfiles.git $HOME/.cfg
config checkout
config config --local status.showUntrackedFiles no
