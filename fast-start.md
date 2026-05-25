```sh
~/.pyenv/versions/3.10.20/bin/python -m venv venv
source venv/bin/activate
pip install "Cython"
pip install numpy==1.23.5
pip install --no-build-isolation madmom
pip install -r requirements.txt
```