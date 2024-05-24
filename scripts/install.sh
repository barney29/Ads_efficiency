#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing Docker..."
    # Install Docker
    sudo apt-get remove docker docker-engine docker.io  containerd runc
    sudo apt install apt-transport-https ca-certificates curl software-properties-common 
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \ "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io

else
    echo "Docker is already installed."
fi

echo "Setting Up Redash local development"


sudo apt -y install build-essential curl docker-compose pwgen python3-venv xvfb


sudo usermod -aG docker $USER
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts 18
nvm alias default 18
nvm use 18

sudo npm install -g yarn@1.22.22

git clone https://github.com/getredash/redash

cd redash
if ! command -v yarn &> /dev/null; then
    sudo npm install --global yarn
fi
yarn
yarn unlink "@redash/viz"
export NVM_DIR="$HOME/.nvm" [ -s "$NVM_DIR/nvm.sh"] && \. "$NVM_DIR/nvm.sh"
nvm install 20.0
nvm use 20.0
nvm alias default 20.0 
yarn build
make compose_build
docker image list
make create_database
make up
