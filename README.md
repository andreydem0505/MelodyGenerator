### Using

#### First launch

Please use `python 3.10`

```sh
~/.pyenv/versions/3.10.20/bin/python -m venv venv
source venv/bin/activate
pip install "Cython"
pip install numpy==1.23.5
pip install --no-build-isolation madmom
pip install -r requirements.txt
```

To see list of available commands type: 
```sh
src/main.py -h
```

### Testing

#### To run unit test test

```sh
pytest
```

#### To run integration test

```sh
venv/bin/python test/generate_analyse_compare.py
```

1. Will be generated --count number of wav files;
2. Then script will analyse them;
3. And compare input parameters with an actual generated files