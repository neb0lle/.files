#!/usr/bin/env bash

rofi_command="rofi -theme ~/.config/rofi/themes/sed.rasi"

uptime=$(uptime -p | sed -e 's/up //g')

# options
shutdown="shutdown"
reboot="reboot"
lock="lock"
suspend="suspend"
logout="logout"

# variable passed to rofi
options="$lock\n$logout\n$shutdown\n$suspend\n$reboot\nFFC-on\nFFC-off"

chosen="$(echo -e "$options" | $rofi_command -p "神  $uptime:" -dmenu)"
case $chosen in
    $shutdown)
        systemctl poweroff
        ;;
    $reboot)
        systemctl reboot
        ;;
    $lock)
        light-locker-command -l
        ;;
    $suspend)
        # amixer set Master mute
        systemctl suspend
        ;;
    $logout)
        qtile cmd-obj -o cmd -f shutdown
        ;;
    'FFC-on')
        nvidia-settings --assign CurrentMetaMode="nvidia-auto-select +0+0 { ForceFullCompositionPipeline = On }"
        ;;
    'FFC-off')
        nvidia-settings --assign CurrentMetaMode="nvidia-auto-select +0+0 { ForceFullCompositionPipeline = Off }"
        ;;
esac
