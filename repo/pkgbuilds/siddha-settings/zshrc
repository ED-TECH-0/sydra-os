# Sydra OS / Siddha Developer Zsh Configuration

# Enable Starship prompt
if command -v starship &>/dev/null; then
    eval "$(starship init zsh)"
fi

# Enable zoxide
if command -v zoxide &>/dev/null; then
    eval "$(zoxide init zsh)"
fi

# History configuration
HISTFILE="$HOME/.zsh_history"
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE

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

# Source plugins if available
[[ -f /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
[[ -f /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] && source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
