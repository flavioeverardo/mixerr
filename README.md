# mixerr
An Answer Set Programming Approach to Explore the Mix Space

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/potassco/xorro)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)


> A system to explore the mix space with representative solutions using ASP.
> Currently working with `clingo` 5.6.2

## Description
Answer Set Programming (ASP) is a rule-based formalism for modeling and solving knowledge-intense combinatorial (optimization) problems with previous works in music-making processes, particularly in composition, little progress has been made in post-production, specifically as it relates to mixing. Automatic multitrack mixing is a developing field under the subject of Intelligent Music Production (IMP) to support or assist mixers by delegating some processes/decisions to intelligent systems. </br>
We present the inclusion of ASP in a system called `mixerr`, an interactive and scalable system capable of exploring through distinct and representative balanced solutions from the mixing space, providing the user, either a professional or student, with reference points to compare and make better and informed decisions. </br>
The system outputs human-readable mixing parameters and visualizations to improve the decision-making process by allowing the mixer to incorporate these starting point settings and refine the generated mix.

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Examples](#examples)
- [Contributors](#contributors)
- [License](#license)


## Requirements

The first generation of `mixerr` works with `clingo` version 5.6.2
and is tested under Unix systems Linux and Mac with Python 3.11.0 </br>
The easiest way to obtain Python enabled `clingo` packages is using Anaconda.
Packages are available in the Potassco channel.
First install either Anaconda or Miniconda and then run: `conda install -c potassco clingo`.</br>
The following python packages must be installed:
- Scipy
- PrettyTable
- Numpy
- Matplotlib
- Tkinter
- PIL
- Pygame


## Usage

To use `mixerr` directly from source run `python -m mixerr` from the project's root directory.</br>
You can run mixerr independently from the player by calling one of these two commands:
```
python -m mixerr --project=Nerve9_PrayForTheRain
python mixerr/player.py --project=Nerve9_PrayForTheRain
```
To execute `mixerr` followed by the `mixerr` player, you can execute a single call:
```
f=Nerve9_PrayForTheRain; python -m mixerr --project=$f && python mixerr/player.py --project=$f
```

To get additional information you can add the `--display` flag on both commands or ask for the general help option with `--help`. 



## Examples

Coming soon...


## Contributors

* Flavio Everardo - Get help/report bugs via the [issue tracker] </br>

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


[issue tracker]: [https://github.com/potassco/xorro/issues](https://github.com/flavioeverardo/mixerr/issues)
