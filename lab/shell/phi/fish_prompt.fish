function fish_prompt
    set -l last_status $status
    set -l cyan (set_color -o cyan)
    set -l violet (set_color -o 8a2be2)
    set -l green (set_color -o green)
    set -l red (set_color -o red)
    set -l blue (set_color -o blue)
    set -l normal (set_color normal)

    set -l username (whoami)
    set -l hostname (hostname -s)

    echo ""
    echo -n -s $violet "┌─[" $cyan $username $violet "@" $cyan $hostname $violet "]─[" $green (pwd | sed "s|^$HOME|~|") $violet "]"
    if set -q SSH_CONNECTION
        echo -n -s "─[" $blue "ssh" $violet "]"
    end
    echo ""

    if test $last_status -eq 0
        echo -n -s $violet "└─" $green "❯ " $normal
    else
        echo -n -s $violet "└─" $red "❯ " $normal
    end
end
