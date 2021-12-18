# PyCASCLib
CASC interface for Warcraft III. This repo provides bindings for JCASC: https://github.com/DrSuperGood/JCASC

# Installation
Jdk is required for installation. You can either download it manually and set jdk_path or let the installer do it automatically.
for windows:
```sh
python setup.py install --new --version=16
```
```sh
python setup.py install --jdkpath "path_to_your_jdk"
```
for unix:
```sh
python3 setup.py install --new --version=16
```
```sh
python3 setup.py install --jdkpath "path_to_your_jdk"
```

# Usage
main functions are: read_temp, open_image, open_file, read_text
```python
from PyCASCLib.storage import read_temp, open_image, open_file, read_text
from pathlib import Path
storage_path = Path('C:/Program Files/Warcraft III')
image_path = 'UI\Widgets\Glues\GlueScreen-Button1-BorderedBackdropBorder-DisabledDown.dds'
image = open_image(storage_path, image_path, is_hd=False)  # returns pil image
```



