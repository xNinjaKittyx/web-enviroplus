# This is not ready yet.

This is a WIP currently. It has no real functionality yet.

The plan is to make an enviroplus REST API webserver so that you can use it to remotely ingest whatever data you want.

Part of this project is also to make installing enviroplus easier... The original project is quite messy due to its 2/3 compatibility and doesn't seem to be very OS-agnostic/friendly in my experience.

This project will be using poetry to manage packages. Feel free to use this pyproject.toml as a starting point

# Pre-requisites
- Python 3.7+
- Poetry

My personal favorite way to install using pyenv + pipx + poetry
```
# Install pyenv on your distro
sudo apt install pyenv
sudo pacman -S pyenv

# Use Pyenv to install a python version.
pyenv install 3.7.6
pyenv shell 3.7.6
pip install pipx
pipx install poetry
```

# Installation
```
git clone https://github.com/xNinjaKittyx/web-enviroplus.git
cd web-enviroplus
poetry install
poetry run webserver  # TODO
```

# Post-Installation
Will require some `/boot/config.txt` changes - TODO
