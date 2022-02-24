#!/bin/sh
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
xss-lock -- ~/.scripts/lockscreen &
nvidia-settings --assign CurrentMetaMode="nvidia-auto-select +0+0 { ForceFullCompositionPipeline = On }" &
xwallpaper --maximize ~/Pictures/Wallpapers/wallpaper.png &
picom --experimental-backends &
sxhkd &
nm-applet &
blueman-applet &
greenclip daemon &
dunst &
flameshot &
udiskie &

xinput set-prop 11 342 1 &
xinput set-prop 11 321 1 &
