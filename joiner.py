import re
from collections import OrderedDict
import os
import sys
import ffmpeg
import argparse

parser = argparse.ArgumentParser(description='Combine and compress GoPro videos into one video.')
parser.add_argument('folder')
parser.add_argument('--scale', default=None, help='hd720, hd1080, 2k, 4k')
parser.add_argument('--fps', default=None, help='hd720, hd1080, 2k, 4k')

class FileRepresentation:
    prefix = None
    video_number = None
    chapter = None
    folder = None
    filename = None
    filepath = None

    def __str__(self):
        return f'filename: {self.filename}, prefix: {self.prefix}, video_number: {self.video_number}, chapter: {self.chapter}'


class Joiner:
    @staticmethod
    def combine_compress_and_rename_videos_in_folder(folder=None, scale=None, fps=None):
        if folder is None:
            print('No folder. return.')
            return

        videos_to_process = []

        for subdir, dirs, files in os.walk(folder):
            for file in sorted(files):
                print(f'file: {file}')

                regex_match = re.match(r"(.*_)(\d{4})_(\d{3})\.mp4", file, re.I)
                if regex_match:
                    print('matched regex 1.')

                    prefix = regex_match.group(1)
                    video_number = regex_match.group(2)
                    chapter = regex_match.group(3)
                else:
                    regex_match = re.match(r"(GP|GH)(\d{2})(\d{4})\.mp4", file, re.I)

                    if regex_match:
                        print('matched regex 2')
                        prefix = regex_match.group(1)
                        video_number = regex_match.group(3)
                        chapter = regex_match.group(2)
                    else:
                        print('did NOT match regex. continue..')
                        continue

                dic = FileRepresentation()
                dic.prefix = prefix
                dic.video_number = video_number
                dic.chapter = chapter
                dic.filename = file
                dic.folder = folder
                dic.filepath = folder + '/' + file

                print(dic)

                videos_to_process.append(dic)

        print('organize into files to combine..')
        organized = OrderedDict()
        for dic in videos_to_process:
            unique_video_key = (dic.prefix, dic.video_number)
            organized.setdefault(unique_video_key, [])
            organized[unique_video_key].append(dic)
            print('done organizing files to combine.')

        print('running ffmpeg on files..')
        for unique_video_key in organized:
            print(f'unique_video_key: {unique_video_key}')

            files_to_combine = []
            for dic in organized[unique_video_key]:
                files_to_combine.append(dic.filepath)
            print(f'files_to_combine: {files_to_combine}')

            ffmpeg_inputs = []
            for file in files_to_combine:
                ffmpeg_inputs.append(ffmpeg.input(file))
                ffmpeg_inputs.append(ffmpeg.input(file))

            d = {'a': 1, 'v': 1}
            joined = ffmpeg.concat(*ffmpeg_inputs, **d)

            if scale is not None:
                joined = ffmpeg.filter(joined, 'scale', size=scale, force_original_aspect_ratio='decrease')

            if fps is not None:
                joined = ffmpeg.filter(joined, 'fps', fps=fps, round='up')

            dic = organized[unique_video_key][0]
            out_path = dic.folder + '/' + dic.prefix + dic.video_number + '_combined.mp4'
            out_stream = ffmpeg.output(joined, out_path)
            out_stream.run()


if __name__ == '__main__':
    parser.print_help()

    args = parser.parse_args()
    Joiner.combine_compress_and_rename_videos_in_folder(args.folder, args.scale, args.fps)
