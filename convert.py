"""Conversion script for your video files."""
import argparse
import os
import ffmpeg

from pathlib import Path
from typing import Union


# Check which types are admissible, these will not be converted if it is not
# necessary.
SUPPORTED_TYPES = {
    'video': {
        'containers':{
            'asf': ['h264', 'mpeg4', 'mjpeg', 'wmv2', 'wmv3'],
            'avi': ['h264', 'mpeg4', 'mjpeg'],
            'mkv': ['h264', 'mpeg4', 'mjpeg'],
            'mp4': ['h264', 'mpeg4'],
            '3gpp': ['h264', 'mpeg4'],
            'mpeg': ['mpeg1video', 'mpeg2video', 'h264'],
            'mpegts': ['mpeg2video', 'h264', 'vc1'],
        }

    },
    'audio': {
        'containers': {
            'asf': ['mp3', 'ac3', 'mwav2', 'wmapro', 'wmavoice'],
            'avi': ['mp3', 'ac3', 'dca'],
            'mkv': ['mp3', 'ac3', 'dca', 'aac'],
            'mp4': ['mp3', 'aac', 'ac3'],
            '3gpp': ['aac'],
            'mpeg': ['ac3', 'mp2', 'mp3', 'aac'],
            'mpegts': ['aac', 'mp3', 'ac3'],
        }
    }
}


# If it does have to be converted, specify the format and extra options here
CONVERT_TO_TYPES = {
    'container': 'mkv',
    'vcodec': 'h264',
    'acodec': 'aac'
}

# Specify a suffix (added before the actual file suffix) to save the new file
NEW_VIDEO_SUFFIX = '.new'


def convert(path: Union[Path, str], dry_run=False, replace=False):
    """Convert a file (if necessary).

    Parameters
    ----------
    path : Union[Path, str]
        The path to convert
    dry_run : bool
        If dry_run is true, no actual conversion will be done
    replace : bool
        Whether to replace the original file with the newly created one
    """
    print(f"Checking {path}...")

    # Check if the path is actually a video
    if path.endswith('txt'):
        print("\tNot a video file, skipping...")
        return
    try:
        info = ffmpeg.probe(path)
    except ffmpeg._run.Error:
        print("\tNot a video file, skipping...")
        return

    # Check whether conversion is necessary
    to_convert = []
    container = os.path.basename(path).split('.')[-1]
    for stream in info['streams']:
        for type_ in ['video', 'audio']:
            if stream['codec_type'] == type_:
                codecs = SUPPORTED_TYPES[type_]['containers'][container]
                # If the codec is not supported, a conversion must happen
                if stream['codec_name'] not in codecs:
                    to_convert += [type_]

    if len(to_convert) == 0:
        print("\tVideo doesn't require conversion, skipping...")
        return
    else:
        print('\t{} needs to be converted'.format(','.join(to_convert)))

    # Specify the options for ffmpeg
    extra_options = {}
    if 'video' in to_convert:
        extra_options['vcodec'] = CONVERT_TO_TYPES['vcodec']
    else:
        extra_options['vcodec'] = 'copy'
    if 'audio' in to_convert:
        extra_options['acodec'] = CONVERT_TO_TYPES['acodec']
    else:
        extra_options['acodec'] = 'copy'

    new_path = ".".join(path.split('.')[:-1]) \
               + NEW_VIDEO_SUFFIX + '.' \
               + CONVERT_TO_TYPES['container']
    # Run ffmpeg
    if not dry_run:
        print('\tStarting FFMPEG conversion...')
        ffmpeg.input(path).output(new_path, **extra_options).run()

    # Check if the original file should be replaced
    if replace:
        os.rename(new_path, path)
        print(f'\tDone! {path}')
    else:
        print(f'\tDone! {new_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert files to a specific format with ffmpeg if if they"
                    " don't comply to certain filetypes/containers/codecs."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=False,
        help='Do a dry run (i.e. no conversion will actually be executed).'
    )
    parser.add_argument(
        '--replace',
        action='store_true',
        default=False,
        help='Replace the original file.'
    )
    parser.add_argument(
        'path',
        help='The folder which contains the files to convert,'
             ' or the file itself.'
    )

    args = parser.parse_args()
    # Check whether a folder or a single file was given.
    if os.path.isdir(args.path):
        for root, dirs, files in os.walk(args.path):
            for file in files:
                convert(
                    os.path.join(root, file),
                    args.dry_run,
                    args.replace
                )
    else:
        convert(args.path, args.dry_run, args.replace)

    print('Conversion completed')