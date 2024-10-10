# Reservoir Sampling

Python implementation of [reservoir sampling](https://en.wikipedia.org/wiki/Reservoir_sampling) a family of randomized algorithms for choosing a simple random sample, without replacement, of k items from a population of unknown size n in a single pass over the items.
The size of the population n is not known to the algorithm and is typically too large for all n items to fit into main memory.
The population is revealed to the algorithm over time, and the algorithm cannot look back at previous items.
At any point, the current state of the algorithm must permit extraction of a simple random sample without replacement of size k over the part of the population seen so far.

## Install

```sh
python3 -m pip install git+https://github.com/SamuelLarkin/reservoir_sampling.git
```

or

```sh
python -m pip install .
```

### One file

[PyInstaller Manual](https://pyinstaller.org/en/stable/index.html)
Install `reservoir-sampling` as a one binary file.

```sh
python -m venv venv
source venv/bin/activate ""
python -m pip install .[install]
pyinstaller --onefile venv/bin/reservoir-sampling
install dist/reservoir-sampling ~/.local/bin/
```
