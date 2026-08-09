function fish_prompt
    set -l last_status $status
    set -l normal (set_color normal)
    set -l cyan (set_color -o cyan)
    set -l red (set_color -o red)

    if test $last_status -eq 0
        echo -n -s $cyan (prompt_pwd) " ❯ " $normal
    else
        echo -n -s $cyan (prompt_pwd) " " $red "❯ " $normal
    end
end
