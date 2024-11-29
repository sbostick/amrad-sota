* https://storage.sota.org.uk/summitslist.csv


Python Virtual Env
------------------

* https://docs.python.org/3/library/venv.html


### Setup venv (one time setup)

```
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
echo "VIRTUAL_ENV is $VIRTUAL_ENV"
```


### Install packages to venv

```
pip install --upgrade pip
pip list
pip install --upgrade ruff pylint pycodestyle pyyaml requests attrs
pip freeze > requirements.txt
```


### Development loop

```
source .venv/bin/activate
echo "VIRTUAL_ENV is $VIRTUAL_ENV"

make
```
