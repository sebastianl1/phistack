# ========================================
# ========================================
fish_add_path $HOME/bin
fish_add_path $HOME/.local/bin

if status is-interactive

    # ========================================
    # Custom Greeting
    # ========================================
    function fish_greeting
        set_color brcyan
        echo "╭──────────────────────────────╮"
        set_color brgreen
        echo "│    ◆ CebacTNaH ◆             │"
        set_color brcyan
        echo "│    Andoideveloper             │"
        set_color brcyan
        echo "╰──────────────────────────────╯"
        set_color normal
    end

    # ========================================
    # Android SDK
    # ========================================
    set -gx ANDROID_HOME $PREFIX/opt/android-sdk
    set -gx ANDROID_SDK_ROOT $ANDROID_HOME
    fish_add_path -g $ANDROID_HOME/cmdline-tools/latest/bin
    fish_add_path -g $ANDROID_HOME/platform-tools

    # ========================================
    # Flutter
    # ========================================
    set -gx FLUTTER_ROOT $PREFIX/opt/flutter
    fish_add_path -g $FLUTTER_ROOT/bin
    set -gx FLUTTER_GIT_URL unknown

    # ========================================
    # Java / Gradle
    # ========================================
    set -gx JAVA_HOME $PREFIX/lib/jvm/java-21-openjdk
    fish_add_path -g $JAVA_HOME/bin

    # ========================================
    # Development Aliases
    # ========================================
    alias nv="nvim"
    alias v="nvim"
    alias lg="lazygit"
    alias gs="git status"
    alias gp="git push"
    alias gc="git commit"
    alias ga="git add"
    alias fl="flutter"
    alias fld="flutter doctor"
    alias flb="flutter build apk --release --target-platform android-arm64"
    alias flr="flutter run -d web-server --web-port 8080"
    alias pn="pnpm"
    alias yr="yarn"
    alias dev="tmux new-session -A -s dev"

    # ========================================
    # Zoxide (smart cd)
    # ========================================
    zoxide init fish | source

    # ========================================
    # Starship Prompt
    # ========================================
    starship init fish | source

    # ========================================
    # Adb over TCP/IP helper
    # ========================================
    function adb-connect
        adb connect $argv[1]:5555
    end

    function adb-wifi
        adb tcpip 5555
        echo "ADB en modo TCP en puerto 5555. Conecta con: adb-connect <ip>"
    end

end

# RANDI - Local AI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434
set -gx RANDI_REPO https://github.com/TU_USUARIO/randi.git

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434
set -gx OLLAMA_FLASH_ATTENTION 1
set -gx OLLAMA_KV_CACHE_TYPE q8_0

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434
set -gx OLLAMA_FLASH_ATTENTION 1
set -gx OLLAMA_KV_CACHE_TYPE q8_0

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434
set -gx OLLAMA_FLASH_ATTENTION 1
set -gx OLLAMA_KV_CACHE_TYPE q8_0

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434
set -gx OLLAMA_FLASH_ATTENTION 1
set -gx OLLAMA_KV_CACHE_TYPE q8_0

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434
set -gx OLLAMA_FLASH_ATTENTION 1
set -gx OLLAMA_KV_CACHE_TYPE q8_0

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434
set -gx OLLAMA_FLASH_ATTENTION 1
set -gx OLLAMA_KV_CACHE_TYPE q8_0

# RANDI
fish_add_path $HOME/bin
set -gx OLLAMA_KEEP_ALIVE -1
set -gx OLLAMA_HOST http://localhost:11434
set -gx OLLAMA_FLASH_ATTENTION 1
set -gx OLLAMA_KV_CACHE_TYPE q8_0
