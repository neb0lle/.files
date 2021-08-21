#!/bin/sh
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
nitrogen --restore &
picom --experimental-backends &
nm-applet &
greenclip daemon &
dunst &
xbindkeys &
flameshot &
noisetorch -i &
setxkbmap -option caps:swapescape &
alttab -font "xft:JetBrainsMono Nerd Font-13" -fg "#ffffff" -bg "#000000" -frame "#ffffff" -t 100x100 -d 1 &
