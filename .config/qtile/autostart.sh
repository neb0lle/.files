#!/bin/sh
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
nitrogen --restore &
picom --experimental-backends &
setxkbmap -option caps:swapescape &
sxhkd &
nm-applet &
greenclip daemon &
dunst &
flameshot &
noisetorch -i &
sleep 5 && alttab -font "xft:JetBrainsMono Nerd Font-11" -fg "#ffffff" -bg "#000000" -frame "#ffffff" -t 100x100 -d 1 &
