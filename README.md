中文版本请参考[这里](./README_CN.md)

# Camera Photo Watermark Generator

ExifWaterMarkMaker is a watermark generator for generating a Xiaomi Camera-like photo watermark style, based on the EXIF information of the camera image, extracting the relevant camera information and rendering it to a new image.

Some watermark generation tools currently in use now have more or less certain problems, such as:

- Not automated enough, requiring the user to fill in several pieces of information;
- The UI of the generated watermark bar is not detailed enough and has a cheap look;
- Does not support reading lens information, or lens information can not be read out;
- There are some problems with UI elements that are not adaptive;
- etc.

In view of the above, we manually wrote a script project to quickly generate the corresponding watermark image.

# Features

ExifWaterMarkMaker has the following features.

1. support drag and drop images/folders to generate processed images with one click (use `pyinstaller` to export), support command line to generate images with one click.
2. support reading camera model, focal length, aperture, shutter, ISO and time.
3. support reading lens model information (tested for Panasonic & Fuji cameras, others to be tested).
4. support automatically embedding the corresponding camera manufacturer's logo.
5. Support adaptive horizontal and vertical screen, UI horizontal and vertical screen automatic adjustment.
6. other features under development...

# Use

Use the following command to install the dependency:

```shell
pip install -r requirements.txt
```

If using the command line to export images, execute:

```shell
python main.py <file_path_1> <file_path_2> <file_path_3> ...
```

If you expect to export an executable, install `pyinstaller`, then export the project executable, finding it in the project `. /dist/` directory to find the corresponding executable:
```shell
# Install the dependencies first
pip install pyinstaller
# Export the executable
pyinstaller --onefile main.py --add-data=./assets/:./assets/
```

# The effect
![](markdown/preview.png)

# More

- Only Panasonic and Fuji cameras are on hand, compatibility with other cameras is to be tested;
- Any problem in using it, please feel free to submit an issue.
