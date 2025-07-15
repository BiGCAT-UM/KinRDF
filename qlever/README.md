# KinRDF Qleverfile

## Python `venv` and `qlever`

Set up a `venve on Debian Testing with:

```shell
python3 -m venv /home/${HOME}/.venvs/qlever
source /home/${HOME}/.venvs/qlever/bin/activate
pip install qlever
```

Assuming you already have `docker` (if not, see below), do:

```shell
qlever get-data --input-files Qleverfile
sudo /home/${HOME}/.venvs/qlever/bin/qlever index --input-files Qleverfile
sudo /home/${HOME}/.venvs/qlever/bin/qlever start --description KinRDF
sudo /home/egonw/.venvs/qlever/bin/qlever ui
```

And then you will have the QLever GUI running.

## Docker on Debian Trixie (Testing)

Follow the instructions here: https://docs.docker.com/engine/install/debian/
