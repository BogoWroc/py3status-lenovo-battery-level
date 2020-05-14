
# py3status-lenovo-battery-level

## requirements
 - Ubuntu + i3wm + py3status
 - Lenovo T470
 
## install

```text
cp lenovo_battery_level.py ~/.i3/py3status  
```

# testing

run the tests with tox:

```console
$ cd </path/to/this/repo>
$ tox
```

## development

install a development environment:

```console
$ cd </path/to/this/repo>
$ tox -e dev
```

... and activate it e.g via `source .tox/dev/bin/activate`. Then run tests with `pytest`.
