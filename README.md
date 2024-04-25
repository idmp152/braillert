![Logo](https://user-images.githubusercontent.com/38213271/219941713-9e801c99-4262-42f1-8fe9-f3c33c66a76b.png)

<div align="center">
  
  # Braillert
  
  <h4>
    Generate braille arts using various palette types.
  </h4>
  
  ![Maintenance](https://img.shields.io/maintenance/yes/2024)
  ![PyPi](https://img.shields.io/pypi/v/braillert)
[![CodeFactor](https://www.codefactor.io/repository/github/idmp152/braillert/badge)](https://www.codefactor.io/repository/github/idmp152/braillert)
  
  [![GitHub stars](https://badgen.net/github/stars/ov3rwrite/braillert)](https://GitHub.com/ov3rwrite/braillert/stargazers/)
  [![GitHub issues](https://badgen.net/github/issues/ov3rwrite/braillert)](https://GitHub.com/ov3rwrite/braillert/issues/)
  ![Commits](https://img.shields.io/github/commit-activity/m/ov3rwrite/braillert)
  
  [![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-383/)
  ![License: MIT](https://img.shields.io/github/license/ov3rwrite/braillert)

  <sub>Built with ❤︎ by
  <a href="https://github.com/idmp152">idmp152</a>

  <sub>
  Readme inspiration:
  <a href="https://github.com/miraclx/freyr-js">freyr-js</a>

</div>

## Demo
  
![Demo](https://user-images.githubusercontent.com/38213271/219941837-089de750-7744-42f3-84e1-2b17d95cdf8b.gif)
  
## Description
  
Braillert is a text art generator using braille symbols. It supports multiple color palettes including 2-color grayscale, extended grayscale, high and low 8-color palette, 16 and 256 color palettes. Can be used either as a CLI program or a library.

## Installation

```cmd
pip install braillert
```

## Usage
```cmd
braillert [-h] -fp FILE_PATH [-m {2,8_lo,8_hi,16,256,gs_ext}] [-w WIDTH] [-o OUT] [-t THRESHOLD] [-dl] [-gf] [-r]
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
- gs_ext (24 color grayscale extended palette)
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
