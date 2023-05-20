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
`mixerr` reads the multitracks from the projects directory. There you can add your directory with all the tracks/stems in wav format. The name of the project is the same as the directory name where your audio files are located. It is recommended to avoid using white spaces in the project name.
It has been tested CD format standard using a sample rate of 44,100 Hz and a bit depth of 16.

<img width="321" alt="project example" src="https://github.com/flavioeverardo/mixerr/assets/29477813/8fda5d29-5482-42dd-a786-ab4baa56b74c">

Similarly, the output is located in the results directory where the player reads the data.

To get additional information you can add the `--display` flag on both commands or ask for the general help option with `--help`. 



## Examples

Here is the complete example from one of the given multitracks.
Open your terminal and run the following command.
```
$ f=Nerve9_PrayForTheRain; python -m mixerr --project=$f && python mixerr/player.py --project=$f
```
The following output will be displayed on screen.
```
Project: Nerve9_PrayForTheRain
Reading audio file: Normalized 1-01_KickIn.wav
Reading audio file: Normalized 11-11_BassDI.wav
Reading audio file: Normalized 12-12_BassAmp.wav
Reading audio file: Normalized 13-13_ElecGtr02.wav
Reading audio file: Normalized 14-14_ElecGtr04.wav
Reading audio file: Normalized 15-15_ElecGtr05.wav
Reading audio file: Normalized 16-16_ElecGtr06.wav
Reading audio file: Normalized 17-17_LeadVox.wav
Reading audio file: Normalized 2-02_KickOut.wav
Reading audio file: Normalized 3-03_Snare.wav
Reading audio file: Normalized 4-04_SnareSample.wav
Reading audio file: Normalized 5-05_Overheads.wav
Reading audio file: Normalized 6-06_Tom1Sample.wav
Reading audio file: Normalized 7-07_Tom2Sample.wav
Reading audio file: Normalized 8-08_Tom3Sample.wav
Number of tracks: 15
Generating mixes...
Calculating distances...
Searching for the optimum grid...
Optimum model found!
Normalizing tracks...
Generating mixes, plans and plots...
Writing the output XML file
pygame 2.4.0 (SDL 2.26.4, Python 3.11.0)
Hello from the pygame community. https://www.pygame.org/contribute.html
Reading the XML file
mixerr
Nerve9_PrayForTheRain
Iniatializing the UI
```
Now the UI is built and it is ready to click on each tile to produce sound.

<img width="499" alt="Nerve9 mixerr" src="https://github.com/flavioeverardo/mixerr/assets/29477813/e9f9d3a5-12aa-4a27-8a7e-e00578efc1bd">

## Contributors

* Flavio Everardo - Get help/report bugs via the [issue tracker] </br>

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


[issue tracker]: [https://github.com/potassco/xorro/issues](https://github.com/flavioeverardo/mixerr/issues)
