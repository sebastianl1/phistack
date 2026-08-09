# PhiStack - config.fish (minimal)
fish_add_path $HOME/.local/bin

if status is-interactive
    # Aliases básicos
    alias nv="nvim"
    alias v="nvim"
    alias lg="lazygit"
    alias gs="git status"
    alias gp="git push"
    alias gc="git commit"
    alias ga="git add"
    alias ls="ls --color=auto"
    alias ll="ls -la"
    alias ..="cd .."
end
