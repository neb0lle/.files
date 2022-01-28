# https://github.com/NevilleJS/dotfiles

from typing import List  # noqa: F401
import os
import subprocess
from libqtile import qtile, bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen

# from libqtile.dgroups import simple_key_binder
from libqtile.command import lazy
from libqtile.lazy import lazy

mod = "mod4"
alt = "mod1"
terminal = "kitty"

# Resize functions for bsp layout
def resize(qtile, direction):
    layout = qtile.current_layout
    child = layout.current
    parent = child.parent
    while parent:
        if child in parent.children:
            layout_all = False
            if (direction == "left" and parent.split_horizontal) or (
                direction == "up" and not parent.split_horizontal
            ):
                parent.split_ratio = max(5, parent.split_ratio - layout.grow_amount)
                layout_all = True
            elif (direction == "right" and parent.split_horizontal) or (
                direction == "down" and not parent.split_horizontal
            ):
                parent.split_ratio = min(95, parent.split_ratio + layout.grow_amount)
                layout_all = True
            if layout_all:
                layout.group.layout_all()
                break
        child = parent
        parent = child.parent


@lazy.function
def resize_left(qtile):
    resize(qtile, "left")


@lazy.function
def resize_right(qtile):
    resize(qtile, "right")


@lazy.function
def resize_up(qtile):
    resize(qtile, "up")


@lazy.function
def resize_down(qtile):
    resize(qtile, "down")


keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "n", lazy.layout.next(), desc="Switch focus to other pane of stack"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key(
        [mod, "shift"],
        "n",
        lazy.layout.client_to_next(),
        desc="move window to next stack",
    ),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, alt], "h", resize_left, desc="Grow window to the left"),
    Key([mod, alt], "l", resize_right, desc="Grow window to the right"),
    Key([mod, alt], "j", resize_down, desc="Grow window down"),
    Key([mod, alt], "k", resize_up, desc="Grow window up"),
    # Rotation of windows
    Key([mod], "r", lazy.layout.rotate(), desc="Rotate windows in Stack mode"),
    Key(
        [mod, "control"], "j", lazy.layout.flip_left(), desc="Flip windows towards left"
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.flip_right(),
        desc="Flip windows towards right",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "y",
        lazy.window.toggle_floating(),
        desc="Toggle floating on focused window",
    ),
    Key(
        [mod, "control"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"
    ),
    # Key([mod], "m", , desc="Toggle Maximize"),
    Key([mod, "shift"], "m", lazy.window.toggle_minimize(), desc="Toggle Minimize"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle next layout"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(), desc="Toggle previous layout"),
    # Qtile
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Group Changer
    Key([mod, "control"], "l", lazy.screen.next_group(), desc="Switch to next group"),
    Key(
        [mod, "control"], "h", lazy.screen.prev_group(), desc="Switch to previous group"
    ),
    Key([mod], "u", lazy.next_urgent(), desc="Switch to urgent window"),
]

# Display kebindings in rofi menu
def show_keys(keys):
    key_help = ""
    keys_ignored = (
        "XF86AudioMute",  #
        "XF86AudioLowerVolume",  #
        "XF86AudioRaiseVolume",  #
        "XF86AudioPlay",  #
        "XF86AudioNext",  #
        "XF86AudioPrev",  #
        "XF86AudioStop",
    )
    text_replaced = {
        "mod4": "[S]",  #
        "control": "[Ctl]",  #
        "mod1": "[Alt]",  #
        "shift": "[Shf]",  #
        "twosuperior": "²",  #
        "less": "<",  #
        "ampersand": "&",  #
        "Escape": "Esc",  #
        "Return": "Enter",  #
    }
    for k in keys:
        if k.key in keys_ignored:
            continue
        mods = ""
        key = ""
        desc = k.desc.title()
        for m in k.modifiers:
            if m in text_replaced.keys():
                mods += text_replaced[m] + " + "
            else:
                mods += m.capitalize() + " + "
        if len(k.key) > 1:
            if k.key in text_replaced.keys():
                key = text_replaced[k.key]
            else:
                key = k.key.title()
        else:
            key = k.key
        key_line = "{:<30} {}".format(mods + key, desc + "\n")
        key_help += key_line

    # debug_print(key_line)  # debug only

    xbind_keys = [
        ["[S] + Space", "Application Launcher"],
        ["[S] + c", "Show Clipboard History"],
        ["[S] + =", "Open Calculator"],
        ["[S] + Return", "Open Terminal"],
        ["[S] + f", "Open File Manager"],
        ["[S] + b", "Open Browser"],
        ["PrtScr", "Fullscreen Screenshot"],
        ["[Ctl] + PrtScr", "Screenshot"],
        ["[S] + Escape", "Powermenu"],
    ]
    for i in xbind_keys:
        key_help += "{:<30} {}".format(i[0], i[1] + "\n")

    return key_help


keys.extend(
    [
        Key(
            [mod],
            "F1",
            lazy.spawn(
                "sh -c 'echo \""
                + show_keys(keys)
                + '" | rofi -dmenu -i -mesg "Keyboard shortcuts"\''
            ),
            desc="Print keyboard bindings",
        )
    ]
)

colors = [
    ["#000000", "#000000"],  # BLACK
    ["#ffffff", "#ffffff"],  # WHITE
    ["#01fdb0", "#01fdb0"],  # MINT
    ["#131519", "#131519"],  # DARK GREY
    ["#46474f", "#46474f"],  # LIGHT GREY
    ["#ffff66", "#ffff66"],  # YELLOW
    ["#ff5555", "#ff5555"],  # SALMON
    ["#2392fb", "#2392fb"],  # BLUE
    ["#ff77cc", "#ff77cc"],  # MAGENTA
]

groups = [
    Group("I", {"layout": "bsp"}),
    Group("II", {"layout": "bsp"}),
    Group("III", {"layout": "bsp"}),
    Group("IV", {"layout": "bsp"}),
    Group("V", {"layout": "bsp"}),
    Group("VI", {"layout": "bsp"}),
    Group("VII", {"layout": "bsp"}),
    Group("VIII", {"layout": "bsp"}),
    Group("IX", {"layout": "bsp"}),
]

# Group hotkeys
for i, j in enumerate(groups, 1):
    keys.append(Key([mod], str(i), lazy.group[j.name].toscreen(toggle=True)))
    keys.append(
        Key([mod, "shift"], str(i), lazy.window.togroup(j.name, switch_group=True))
    )

layout_theme = {
    "border_width": 1,
    "margin": 4,
    "border_normal": "131519",
    "border_focus": "46474f",
    "grow_amount": 4,
}
layouts = [
    layout.Bsp(**layout_theme, fair=False, name=""),
    layout.Stack(num_stacks=1, **layout_theme, name="洛"),
    layout.Stack(num_stacks=2, **layout_theme, name=""),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Medium",
    fontsize=14,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    background=colors[3],
                    foreground=colors[3],
                    linewidth=4,
                ),
                widget.GroupBox(
                    font="Nimbus Sans, Bold",
                    padding=4,
                    margin_y=5,
                    fontsize=16,
                    highlight_color=colors[5],
                    block_highlight_text_color=colors[6],
                    inactive=colors[4],
                    active=colors[1],
                    this_current_screen_border=colors[3],
                    disable_drag=True,
                    this_screen_border=colors[3],
                    other_current_screen_border=colors[3],
                    other_screen_border=colors[3],
                    background=colors[3],
                    urgent_text=colors[5],
                    urgent_border=colors[3],
                ),
                widget.WindowName(
                    padding=10,
                    background=colors[3],
                ),
                widget.Sep(
                    background=colors[3],
                    foreground=colors[3],
                    linewidth=8,
                ),
                widget.Systray(
                    background=colors[3],
                    padding=10,
                ),
                widget.Sep(
                    background=colors[3],
                    foreground=colors[3],
                    linewidth=8,
                ),
                widget.TextBox(
                    text="|",
                    background=colors[3],
                    foreground=colors[4],
                    padding=-3,
                    fontsize=20,
                ),
                widget.CurrentLayout(
                    fontsize=20,
                    foreground=colors[1],
                    background=colors[3],
                ),
                widget.Sep(
                    background=colors[3],
                    foreground=colors[3],
                    linewidth=1,
                ),
                # widget.TextBox(
                #     text="|",
                #     background=colors[3],
                #     foreground=colors[4],
                #     padding=-3,
                #     fontsize=20,
                # ),
                # widget.TextBox(
                #     text=" ",
                #     background=colors[3],
                #     foreground=colors[4],
                #     padding=0,
                #     fontsize=20,
                #     mouse_callbacks={
                #         "Button1": lambda: qtile.cmd_spawn("dunstctl history-pop"),
                #         "Button2": lambda: qtile.cmd_spawn(
                #             "dunstctl set-paused toggle"
                #         ),
                #         "Button3": lambda: qtile.cmd_spawn("dunstctl history-pop"),
                #     },
                # ),
                widget.TextBox(
                    text="|",
                    background=colors[3],
                    foreground=colors[4],
                    padding=-3,
                    fontsize=20,
                ),
                widget.TextBox(
                    text="  ",
                    foreground=colors[8],
                    background=colors[3],
                    padding=-3,
                    fontsize=16,
                ),
                widget.Volume(
                    background=colors[3],
                    foreground=colors[8],
                    padding=8,
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            terminal + " /home/neville/.scripts/resize_fixer pulsemixer"
                        )
                    },
                ),
                widget.TextBox(
                    text="|",
                    background=colors[3],
                    foreground=colors[4],
                    padding=-3,
                    fontsize=20,
                ),
                widget.TextBox(
                    text="  ",
                    foreground=colors[2],
                    background=colors[3],
                    padding=0,
                    fontsize=14,
                ),
                widget.CPU(
                    foreground=colors[2],
                    background=colors[3],
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(terminal + " bashtop")
                    },
                    padding=8,
                ),
                widget.TextBox(
                    text="|",
                    background=colors[3],
                    foreground=colors[4],
                    padding=-3,
                    fontsize=20,
                ),
                widget.TextBox(
                    text="  ",
                    foreground=colors[5],
                    background=colors[3],
                    padding=0,
                    fontsize=14,
                ),
                widget.Memory(
                    measure_mem="M",
                    foreground=colors[5],
                    background=colors[3],
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            terminal + " /home/neville/.scripts/resize_fixer htop"
                        )
                    },
                    padding=8,
                ),
                widget.TextBox(
                    text="|",
                    background=colors[3],
                    foreground=colors[4],
                    padding=-3,
                    fontsize=20,
                ),
                widget.TextBox(
                    text="  ",
                    foreground=colors[7],
                    background=colors[3],
                    padding=0,
                    fontsize=14,
                ),
                widget.Clock(
                    foreground=colors[7],
                    background=colors[3],
                    format="%A %B %d - %H:%M",
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            "/home/neville/.scripts/cal_notify"
                        ),
                        "Button3": lambda: qtile.cmd_spawn(
                            terminal + " /home/neville/.scripts/resize_fixer calcurse"
                        ),
                    },
                ),
                widget.TextBox(
                    text="|",
                    background=colors[3],
                    foreground=colors[4],
                    padding=-3,
                    fontsize=20,
                ),
                widget.Battery(
                    foreground=colors[1],
                    background=colors[3],
                    format="{percent:1.0%}"
                        ),
                widget.TextBox(
                    text="|",
                    background=colors[3],
                    foreground=colors[4],
                    padding=-3,
                    fontsize=20,
                ),
                widget.QuickExit(
                    default_text="⏻ ",
                    countdown_format="{}",
                    countdown_start=4,
                    foreground=colors[6],
                    background=colors[3],
                    padding=10,
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            "/home/neville/.scripts/powermenu"
                        ),
                        "Button3": lambda: qtile.cmd_spawn(
                            "/home/neville/.scripts/notifications_toggle" 
                        ),
                    },
                ),
            ],
            30,
            # opacity=0.6,
            margin=[6, 6, 2, 6],
        ),
        bottom=bar.Gap(2),
        left=bar.Gap(2),
        right=bar.Gap(2),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        Match(wm_type="utility"),
        Match(wm_type="notification"),
        Match(wm_type="toolbar"),
        Match(wm_type="splash"),
        Match(wm_type="dialog"),
        Match(wm_class="file_progress"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Qalculate"),
        Match(func=lambda c: c.has_fixed_size()),  # mpv fix
    ]
)

# Configuration Variables
# dgroups_key_binder = simple_key_binder(mod) # make fix & contrib
dgroups_key_binder = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
auto_minimize = True
focus_on_window_activation = "focus"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


wmname = "LG3D"
