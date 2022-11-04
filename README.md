![Logo](https://media.discordapp.net/attachments/955362477137362954/989621188630282290/unknown.png?width=1440&height=255)

<div align="center">
  
  # Braillert
  
  <h4>
    Generate braille arts using various palette types.
  </h4>
  
  ![Maintenance](https://img.shields.io/maintenance/yes/2022)
  ![PyPi](https://img.shields.io/pypi/v/braillert)
  ![CodeFactor](https://www.codefactor.io/repository/github/ov3rwrite/braillert/badge)
  
  [![GitHub stars](https://badgen.net/github/stars/ov3rwrite/braillert)](https://GitHub.com/ov3rwrite/braillert/stargazers/)
  [![GitHub issues](https://badgen.net/github/issues/ov3rwrite/braillert)](https://GitHub.com/ov3rwrite/braillert/issues/)
  ![Commits](https://img.shields.io/github/commit-activity/m/ov3rwrite/braillert)
  
  [![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-383/)
  ![License: MIT](https://img.shields.io/github/license/ov3rwrite/braillert)

  <sub>Built with ❤︎ by
  <a href="https://github.com/ov3rwrite">ov3rwrite</a>

  <sub>
  Readme inspiration:
  <a href="https://github.com/miraclx/freyr-js">freyr-js</a>

</div>

## Demo
  
![Demo](https://media.discordapp.net/attachments/955362477137362954/992127994120392744/braillert.gif?width=729&height=655)
  
## Description
  
Braillert is a text art generator using braille symbols. It supports multiple color palettes including Rich, Colorama and ANSI(Discord). Can be used either as a CLI program or a library.

## Installation

```cmd
pip install braillert
```

## Usage
```cmd
braillert [-h] -fp FILE_PATH [-m {rich,colorama,discord,gs}] [-w WIDTH] [-o OUT] [-c CONTRAST] [-t THRESHOLD]
```
##
`--file-path` or `-fp` - a required argument that represents the path where the convertible image is located e.g.
```
-fp=art.png
```
##
`--mode` or `-m` - a required argument that represents the mode in which the provided image should be converted e.g.
```
--mode=2
```
or
```
-m=8_lo
```
Available modes:
- 2 (grayscale)
- 8_lo (lower 8 colors)
- 8_hi (higher 8 colors)
- 16 (16 colors palette)
- 256 (full colors palette)
##
`--width` or `-w` - an optional argument that represents the width in which the provided image should be resized e.g.
```
--width=150
```
##
`--out` or `-o` - an optional argument that represents the path in which the art should be saved e.g
```
--out=./art.ansi
```
##
`--threshold` or `-t` - an optional argument that represents the threshold value that will be used
during the art generation e.g.
```
--threshold=130
```
## Documentation
Still WIP but a small documentation on each file is available using pydoc.
(every public class and function also has annotations and docstrings)
