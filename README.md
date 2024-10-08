# Quick Installation Guide

## Main Face Recognition Module
 
This Project is under development
---
# Pre-Requirements
##  - `The libraries in requirements.txt`
##  - `dlib With or without CUDA enabled (we recommend enable CUDA support)`
---
# **1** Instaling requirements.txt
## If you want to use dlib with CUDA support, use requirements_wo_dlib.txt
## ```pip install -r requirements.txt``` or ```pip install -r requirements_wo_dlib.txt```
## If you DONT want to use dlib with CUDA support, jump to step **4**
---
# **2** Instaling dlib on Windows with CUDA enabled
# **Video Step by Step Guide (Portuguese)** ---> [link](https://youtu.be/HVBN_PhKGU8) 
# **2.1** Install these pre-requirements:
## - [Visual Studio](https://visualstudio.microsoft.com/pt-br/) and C++ Build Tools
## - CUDA [ToolKit](https://developer.nvidia.com/cuda-downloads)
## - dlib from [github](https://github.com/davisking/dlib/releases/tag/v19.24.2)
## - [Anaconda3](https://www.anaconda.com/download) or [miniconda3](https://docs.conda.io/en/latest/miniconda.html)
## - [cudnn](https://developer.nvidia.com/downloads/compute/cudnn/secure/8.9.3/local_installers/12.x/cudnn-windows-x86_64-8.9.3.28_cuda12-archive.zip/) (just copy cudnn inside /anaconda3/ and /anaconda3/bin/)
## - [CMake](https://cmake.org/download/#latest)

# **2.2** Configuring dlib
## - `Unzip dlib folder anywhere`
## - `Create "build" folder inside dlib folder (path/to/your/dlib/build/)`
## - `Configure dlib with CMake`
## - `Open CMake GUI`
## - `Set: where is the source code: /path/to/your/dlib`
## - `Set: wheres to build the binaries: /path/to/your/dlib/build`
## - `Click "Configure" Button and just press oK or Continue`
## - `When finish the process will apear the dlib's variables`
## - `Seacrh for DLIB_USE_CUDA and check the box or set to "ON"`
## - `Click "Configure" and wait, when its done, should apear "DLIB WILL USE CUDA"`
## ![Image](https://i.imgur.com/e7HcFjV.png)

# **2.3** Install dlib in conda
## - Go to dlib's folder with anaconda terminal (like ```conda cd your/path/to/dlib``` )
## - Execute ```python setup.py install```
## - `Will install dlib in your conda, this will dont work if you dont have cudnn inside conda`
## - `Like before, should apear "DLIB WILL USE CUDA"`
## - `DONT FORGET: TEST DLIB BEFORE USE IT`
## - run a python file with this:
```
import dlib
print(dlib.DLIB_USE_CUDA)
```
## - if you get True, enjoy
---
# **3** Instaling dlib on Linux with CUDA enabled
## [Guide Here](https://gist.github.com/nguyenhoan1988/ed92d58054b985a1b45a521fcf8fa781)
---
# **4** Using Face Recognition System
## - After installing dlib and other libraries from requirements.txt, you just need to run "main.py"
---
