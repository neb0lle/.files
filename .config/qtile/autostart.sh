#!/bin/sh
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
nitrogen --restore &
picom --experimental-backends &
nm-applet &
greenclip daemon &
dunst &
sxhkd &
flameshot &
noisetorch -i &
setxkbmap -option caps:swapescape &
sleep 5 && alttab -font "xft:JetBrainsMono Nerd Font-11" -fg "#ffffff" -bg "#000000" -frame "#ffffff" -t 100x100 -d 1 &
