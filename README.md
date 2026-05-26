### Using

#### First launch

Please use `python 3.10` (if doesn't work try python 3.8)

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
venv/bin/python src/main.py -h
```

### Testing

#### To run unit test

```sh
pytest
```

#### To run integration test

```sh
venv/bin/python test/generate_analyse_compare.py
```

1. Will be generated --count number of .wav files;
2. Then script will analyse them;
3. And compare input parameters with an actual generated files.


---

<img width="1437" height="869" alt="result" src="https://github.com/user-attachments/assets/ea362af9-b43b-4884-91be-41b8fdcb6ce7" />

<ADD DESCRIPTION>

<img width="600" height="600" alt="circle" src="https://github.com/user-attachments/assets/233371ca-96b9-4473-97a0-a013f8974014" />

<ADD DESCRIPTION>
