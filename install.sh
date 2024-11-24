#!/bin/bash

set -e

INSTALL_DIR="/usr/share/doc/torward"
BIN_DIR="/usr/bin/"
MAIN_SCRIPT="src/main.py"

echo "[*] Checking Internet Connection ..."
wget -q --tries=10 --timeout=20 --spider https://google.com
if [[ $? != 0 ]]; then
    echo "Please check your Internet connection and try again."
    exit 1
fi

echo "[✔] Internet connection is good."

# Install required dependencies
echo "[*] Installing required packages..."
if command -v apt-get > /dev/null; then
    sudo apt-get update && sudo apt-get install -y tor python3-pip git
elif command -v pacman > /dev/null; then
    sudo pacman -Suy --noconfirm
    sudo pacman -S --noconfirm tor python-pip git
else
    echo "Unsupported package manager. Please install Tor, Python3-pip, and Git manually."
    exit 1
fi

# Clone or update the repository
if [ -d "$INSTALL_DIR" ]; then
    echo "[!] Torward is already installed. Do you want to update it? [y/n]:"
    read input
    if [ "$input" = "y" ]; then
        cd "$INSTALL_DIR"
        sudo git pull origin main
        echo "[✔] Torward has been updated."
    else
        echo "[!] Installation aborted."
        exit
    fi
else
    echo "[*] Installing Torward..."
    sudo git clone https://github.com/chundefined/Torward.git "$INSTALL_DIR"
fi

# Install dependencies
echo "[*] Installing Python dependencies..."
sudo pip3 install -r "$INSTALL_DIR/requirements.txt"

# Create a command to run Torward
echo "[*] Setting up the torward command..."
echo "#!/bin/bash
python3 $INSTALL_DIR/$MAIN_SCRIPT" '${1+"$@"}' > torward
sudo chmod +x torward
sudo mv torward "$BIN_DIR"

# Create a command to update Torward
echo "[*] Setting up the torward-update command..."
echo "#!/bin/bash
if [ -d \"$INSTALL_DIR\" ]; then
    cd \"$INSTALL_DIR\"
    sudo git pull origin main
    echo \"[*] Updating dependencies...\"
    sudo pip3 install -r requirements.txt
    echo \"[✔] Torward has been updated successfully.\"
else
    echo \"Torward is not installed. Please install it first.\"
fi" > torward-update
sudo chmod +x torward-update
sudo mv torward-update "$BIN_DIR"

echo "[✔] Torward has been installed successfully."
echo "Run 'torward' to start the tool."
echo "Run 'torward-update' to update it to the latest version."
