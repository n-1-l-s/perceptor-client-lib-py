## Tests

## Run unit tests
(must run from virtual env)
Before running, ensure all packages are installed:
```
pip install -r .\test\requirements.txt
```

Run the tests:

On Windows: before running tests, you have to make sure _poppler_ is available on the machine. If the path to _poppler_ is not specified in PATH,
then you have to set the environment variable "_POPPLER_PATH_" to the _poppler_'s directory:
```powershell
$Env:POPPLER_PATH='_path_to_popplers_dir'
```

On linux, make sure the _poppler-utils_ is installed:
```bash
sudo apt-get update
sudo apt-get install poppler-utils -yqq
```

Running the tests:
```
python -m unittest -v
```

Before running the tests from PyCharm (Windows):
Copy the contents of the poppler's "Library/bin" directory into "Poppler_Bin".



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
