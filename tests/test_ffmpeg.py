import unittest
import ffmpeg
import os
import joiner


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_fileloop():
        joiner.Joiner.combine_compress_and_rename_videos_in_folder('.')

    @staticmethod
    def test_combine_scale_and_change_framerate():
        folder = os.path.dirname(os.path.abspath(__file__))
        filename_1 = 'GP021234.mp4'
        filename_2 = 'GH011234.mp4'

        in_path_1 = folder + '/' + filename_1
        in_path_2 = folder + '/' + filename_2
        out_path = folder + '/combine_test.mp4'

        stream_1 = ffmpeg.input(in_path_1)
        stream_2 = ffmpeg.input(in_path_2)
        joined = ffmpeg.concat(stream_1, stream_2)

        joined = ffmpeg.filter(joined, 'scale', size='hd720', force_original_aspect_ratio='decrease')
        joined = ffmpeg.filter(joined, 'fps', fps=25, round='up')

        out_stream = ffmpeg.output(joined, out_path)
        ffmpeg.run(out_stream)


if __name__ == '__main__':
    unittest.main()
