<h1 align="center">CLI Tool for Query Logged Events.</h1>

<p align="center">
  <br>
  <img src="./static/shell-intro.png" alt="QShell Intro" width="500px" height="300px"/>
  <br><br>
  <i>QShell is an interactive command-line interface tool that provides support for a user to query logged events generated during the validation phase of the data extracted by an ETL process.</i>
  <br>
</p>  
<br><br>  

# _Table of Contents_

- [Introduction](#intro)
- [Installation](#install)
- [Technologies](#techno)
- [How it works](#usage)
- [License](#license)

<br>

<a id='intro'></a>
# Introduction

<a id='install'></a>
# Installation
To run the application the `python` interpreter need to be installed. Download or clone the repo and that's it.  
The interactive shell is launched from the `run.py` script. You can refer to "How it works" section for further information on the usage of the application.

<a id='techno'></a>
# Technologies
- Python 3.10.1

<a id='usage'></a>
# How it works

The application performs user's queries on logged events which are loaded from a log file. Then before to run the interactive shell a log file name must be provided to be loaded by the application. The application read and write all files from the "data" folder, so a file needs to be loaded the file has to be put in the "data" folder.  
<br>
<img src="./static/start-load-log.png" alt="QShell Intro"/>
<br>

All search criteria for query the logged events use a subcommand called "query". Typing the subcommand and --help the man page is displayed on the screen.

<br>
<img src="./static/query-help.png" alt="QShell Intro"/>
<br>




---
<a id='license'></a>
# License
### MIT