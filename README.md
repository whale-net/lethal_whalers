lethal company modpack using github actions to submit it

Uses a basic python api client to submit and update
Python client is hand-crafted as openapi spec was unable to produce code

## python setup
install pyenv https://github.com/pyenv/pyenv
```
pyenv virtualenv 3.11.4 lethal_whalers
```
```
pyenv local lethal_whalers
```
following should should display `lethal_whalers (set by /home/user/lethal_whalers/.python-version)`
```
pyenv version
```

using poetry for once
```
pip install poetry
```

install dependencies
```
poetry install
```