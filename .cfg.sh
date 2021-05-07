#!/bin/sh
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
echo "alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'" >> $HOME/.bashrc
echo ".cfg" >> .gitignore
git clone --bare git@github.com:NevilleJS/dotfiles.git $HOME/.cfg
mkdir -p .config-backup && \
config checkout 2>&1 | egrep "\s+\." | awk {'print $1'} | \
xargs -I{} mv {} .config-backup/{}
config checkout
config config --local status.showUntrackedFiles no
