#!/bin/bash

progress_bar() {
    local duration=$1
    local step=$((100 / duration))
    local progress=0

    echo -ne "["
    for ((i=0; i<duration; i++)); do
        sleep 0.1
        progress=$((progress + step))
        echo -ne "#"
    done
    echo -ne "] $progress%\n"
}

# Check if python 3.10 is available
echo -n "Checking for Python 3.10... "
if command -v python3.10 &>/dev/null; then
    progress_bar 10
    echo "✅ Python 3.10 is installed."
else
    progress_bar 10
    echo "❌ Python 3.10 is NOT installed."
    exit 1
fi

# check if venv is available
echo -n "Checking if venv module is available... "
if python3.10 -m venv --help &>/dev/null; then
    progress_bar 10
    echo "✅ venv module is available."
else
    progress_bar 10
    echo "❌ venv module is NOT available."
    echo "Please install it using: sudo apt install python3.10-venv (or equivalent for your distro)"
    exit 1
fi

python3.10 -m venv .myenv

# identify the shell and activate the virtual environment
if [[ "$SHELL" == *"bash"* || "$SHELL" == *"zsh"* ]]; then
    echo "Activating virtual environment for Bash/Zsh..."
    source .myenv/bin/activate
elif [[ "$SHELL" == *"fish"* ]]; then
    echo "Activating virtual environment for Fish shell..."
    source .myenv/bin/activate.fish
elif [[ "$SHELL" == *"csh"* || "$SHELL" == *"tcsh"* ]]; then
    echo "Activating virtual environment for C shell..."
    source .myenv/bin/activate.csh
else
    echo "Shell not recognized. Please manually activate your virtual environment."
    echo "Typically, you can activate it by running one of the following commands:"
    echo "  Bash/Zsh: source .myenv/bin/activate"
    echo "  Fish: source .myenv/bin/activate.fish"
    echo "  C shell: source .myenv/bin/activate.csh"
fi



# update pip
echo -n "Upgrading pip... "
progress_bar 20
pip install --upgrade pip &>/dev/null
echo "✅ Pip upgraded successfully."

# pip install dependencies
if [ -f "requirements.txt" ]; then
    echo -n "Installing dependencies... "
    pip install -r requirements.txt &>/dev/null
    echo "✅ Dependencies installed successfully."
else
    echo "⚠️ No requirements.txt found. Skipping dependency installation."
fi

echo "🎉 Setup completed successfully!"

