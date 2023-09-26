## Tests

## Run unit tests
(must run from virtual env)
Before running, ensure all packages are installed:
```
pip install -r .\test\requirements.txt
```

Run the tests:
```
python -m unittest -v
```


## Packaging

### Build package

In project root:

```
python3 -m build
```

The created package is per default placed in "dist/" subfolder.


### Install local package
```
pip install path_to_package_file
```

## Gitlab registry

[Package Registry](https://gitlab.com/tamedai/perceptor/perceptor-client-lib-py/-/packages) contains the list of available (built) packages.
