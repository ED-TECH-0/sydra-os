# Sydra OS / Siddha Developer Bash Configuration

# Enable Starship prompt
if command -v starship &>/dev/null; then
    eval "$(starship init bash)"
fi

# Enable zoxide
if command -v zoxide &>/dev/null; then
    eval "$(zoxide init bash)"
fi

# History configuration
HISTSIZE=10000
HISTFILESIZE=20000
shopt -s histappend

# Sydra OS Aliases
alias update='siddha-update'
alias rollback='siddha-rollback'
alias dev='siddha-dev'
alias gamehub='siddha-gamehub'

# Modern CLI tools
alias ll='eza -lh --icons 2>/dev/null || ls -lh'
alias la='eza -lha --icons 2>/dev/null || ls -lha'
alias gs='git status -s'
alias gd='git diff'
alias gc='git commit -v'
alias gp='git push'
alias cat='bat 2>/dev/null || cat'
