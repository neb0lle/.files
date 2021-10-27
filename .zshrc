# SED zsh config

# tmux
if command -v tmux &> /dev/null && [ -n "$PS1" ] && [[ ! "$TERM" =~ screen ]] && [[ ! "$TERM" =~ tmux ]] && [ -z "$TMUX" ]; then
	exec tmux -u new-session
fi

# Enable colors and change prompt:
autoload -U colors && colors
PS1="%F{yellow}%n%f%F{magenta}@%f%F{blue}%m%f %~ %F{green}❯%f "

# History:
HISTSIZE=5000
SAVEHIST=5000
HISTFILE=~/.zsh_history

# Basic auto/tab complete:
autoload -U compinit
zstyle ':completion:*' menu select
zmodload zsh/complist
compinit
_comp_options+=(globdots)   # Include hidden files.

# VI mode:
bindkey -v
export KEYTIMEOUT=1

bindkey -M menuselect 'h' vi-backward-char
bindkey -M menuselect 'k' vi-up-line-or-history
bindkey -M menuselect 'l' vi-forward-char
bindkey -M menuselect 'j' vi-down-line-or-history
bindkey -v '^?' backward-delete-char

# Change cursor shape for different vi modes:
function zle-keymap-select {
  if [[ ${KEYMAP} == vicmd ]] ||
     [[ $1 = 'block' ]]; then
    echo -ne '\e[1 q'
  elif [[ ${KEYMAP} == main ]] ||
       [[ ${KEYMAP} == viins ]] ||
       [[ ${KEYMAP} = '' ]] ||
       [[ $1 = 'beam' ]]; then
    echo -ne '\e[5 q'
  fi
}
zle -N zle-keymap-select
zle-line-init() {
    zle -K viins # initiate `vi insert` as keymap (can be removed if `bindkey -V` has been set elsewhere)
    echo -ne "\e[5 q"
}
zle -N zle-line-init
echo -ne '\e[5 q' # Use beam shape cursor on startup.
preexec() { echo -ne '\e[5 q' ;} # Use beam shape cursor for each new prompt.

# Edit line in vim:
autoload edit-command-line; zle -N edit-command-line
bindkey '^e' edit-command-line

# Archive extraction:
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1   ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *.deb)       ar x $1      ;;
      *.tar.xz)    tar xf $1    ;;
      *.tar.zst)   unzstd $1    ;;
      *)           echo "'$1' cannot be extracted" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

# Open ranger in current directory:
run_ranger () {
    echo
    ranger --choosedir=$HOME/.rangerdir < $TTY
    LASTDIR=`cat $HOME/.rangerdir`
    cd "$LASTDIR"
    zle reset-prompt
}
zle -N run_ranger
bindkey '^f' run_ranger

# Resizing issue fix
unset LINES
unset COLUMNS

# EXPORTS
export LANG=en_US.UTF-8
export TERM='screen-256color'
export EDITOR='nvim'
export VISUAL='nvim'
export MANPAGER='nvim +Man!'
export BROWSER='brave'
export TRUEBROWSER='brave'
export BAT_THEME='base16-256'

# PATH
# export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"
# export PATH="/opt/homebrew/opt/util-linux/sbin:$PATH"
path+=("$HOME/.scripts")
export PATH

# aliases
alias vim='nvim'
alias ls='ls -Gh --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias wiki='vim -c ":VimwikiIndex"'
alias py='python3'
alias cf='cowsay "sed"'
alias mute='dunstctl set-paused toggle'
alias config='/usr/bin/git --git-dir=/home/neville/.cfg/ --work-tree=/home/neville'

# fzf
# [ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
source /usr/share/fzf/key-bindings.zsh
source /usr/share/fzf/completion.zsh
export FZF_DEFAULT_COMMAND='ag --hidden -p .gitignore -g ""'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_DEFAULT_OPTS='--height 50% --layout=reverse --border --info=inline --preview "bat --color=always --style=numbers --line-range=:500 {}"'

# Startup
eval "$(starship init zsh)"

# Load zsh-syntax-highlighting; should be last.
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh 2>/dev/null
# source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
