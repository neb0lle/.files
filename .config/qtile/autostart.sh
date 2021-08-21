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
