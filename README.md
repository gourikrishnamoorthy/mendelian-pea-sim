# Mendelian Pea Simulator

A simple python simulator for generating and analysing Pea populations based on External influences.

## Installation

Export the Python path specifing the location of the files.

```bash
export PYTHONPATH=$PYTHONPATH:<Location of the Git clone>>
```

To run the script

``` bash
python ./run.py -i <CONFIG File>
```

To use pip3 for installation

```bash
cd <BASE>/dist
pip3 install Mendelian_Pea-1.0-py3-none-any.whl
```


## Usage

```
(base) gourik$ python run.py -h
usage: run.py [-h] [--version] -i INPUT_FILE

Meandeian Pea Simulator.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -i INPUT_FILE, --input INPUT_FILE
                        Input json file with config params    
```
You can find sample config files under the input folder

## Links
Please find a short blog exploring the implications of the results from the experiments below:
https://medium.com/@gouri.k_20974/evolution-of-a-mendelian-pea-part-2-5a729eddd337

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GPL 2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
