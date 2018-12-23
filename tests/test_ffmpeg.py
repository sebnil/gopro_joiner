import unittest
import os
import joiner


class MyTestCase(unittest.TestCase):
    folder = os.path.dirname(os.path.abspath(__file__))

    def test_combine_compress_and_rename_videos_in_folder(self):
        output_file = self.folder + '/GH1234_combined.mp4'
        try:
            os.remove(output_file)
        except FileNotFoundError:
            pass

        joiner.Joiner.combine_compress_and_rename_videos_in_folder('.')
        self.assertTrue(os.path.exists(output_file))


if __name__ == '__main__':
    unittest.main()
