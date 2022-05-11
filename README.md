Automatic video file converter using FFMPEG
===========================================

You can use the [convert.py](convert.py) script to convert all video files in
a folder structure (or a single file).

## Installation

Currently, the only dependencies are `ffmpeg` and `ffmpeg-python`.

For example, on Ubuntu, you should run

```bash
# Install ffmpeg
sudo apt update && sudo apt install ffmpeg

# Install ffmpeg-python
pip3 install ffmpeg-python
# OR: Install ffmpeg-python through requirements.txt
pip3 install -r requirements.txt
```

## Command line usage

```
usage: convert.py [-h] [--dry-run] [--replace] path

Convert files to a specific format with ffmpeg if if they don't comply to
certain filetypes/containers/codecs.

positional arguments:
  path        The folder which contains the files to convert, or the file
              itself.

optional arguments:
  -h, --help  show this help message and exit
  --dry-run   Do a dry run (i.e. no conversion will actually be executed).
  --replace   Replace the original file.

```

## Adjustments

If you want to adjust the permissible containers/formats/codecs, you will need
to adjust the `SUPPORTED_TYPES` variable in [convert.py](convert.py).

You can define the filetype to convert to with `CONVERT_TO_TYPES`

Finally, you can add a suffix to the newly created files by adjusting
`NEW_VIDEO_SUFFIX`.
