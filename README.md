# CETONI SiLA 2 I/O SDK
## Installation
Run `pip install .` from the root directory containing the file `setup.py`

## Usage
Run `python -m sila_cetoni_io --help` to receive a full list of available options

## Code generation
```console
$ python -m sila2.code_generator new-package -n io_service -o ./sila_cetoni/io/sila/ ./sila_cetoni/io/features*.sila.xml
```
