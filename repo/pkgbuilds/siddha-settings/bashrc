# /etc/profile.d/siddha.sh - Sydra OS environment and shell settings

# 1. Non-interactive shells: return immediately (prevents session startup errors)
case "$-" in
    *i*) ;;
      *) return 0 2>/dev/null || exit 0 ;;
esac

# 2. Add local bin paths
if [ -d "$HOME/.local/bin" ]; then
    case ":$PATH:" in
        *":$HOME/.local/bin:"*) ;;
        *) export PATH="$HOME/.local/bin:$PATH" ;;
    esac
fi

# 3. Sydra OS Aliases
alias update='siddha-update'
alias rollback='siddha-rollback'
alias dev='siddha-dev'
alias gamehub='siddha-gamehub'

# Modern CLI tools aliases
if command -v eza >/dev/null 2>&1; then
    alias ll='eza -lh --icons'
    alias la='eza -lha --icons'
else
    alias ll='ls -lh'
    alias la='ls -lha'
fi

alias gs='git status -s'
alias gd='git diff'
alias gc='git commit -v'
alias gp='git push'

if command -v bat >/dev/null 2>&1; then
    alias cat='bat'
fi

# 4. Interactive prompt initialization per shell
if [ -n "$BASH_VERSION" ]; then
    HISTSIZE=10000
    HISTFILESIZE=20000
    shopt -s histappend 2>/dev/null || true
    if command -v starship >/dev/null 2>&1; then
        eval "$(starship init bash)"
    fi
    if command -v zoxide >/dev/null 2>&1; then
        eval "$(zoxide init bash)"
    fi
elif [ -n "$ZSH_VERSION" ]; then
    if command -v starship >/dev/null 2>&1; then
        eval "$(starship init zsh)"
    fi
    if command -v zoxide >/dev/null 2>&1; then
        eval "$(zoxide init zsh)"
    fi
fi
