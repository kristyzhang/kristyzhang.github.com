__author__ = 'mlwei'

import logging
import os
import shutil
import subprocess
from PythonMagick import Image

class ImageProcessor(object):
    _CONVERT_COMMAND = '/usr/bin/convert'
    _IDENTIFY_COMMAND = '/usr/bin/identify'
    _QUALITIES = [40, 50, 60, 70, 80, 83, 86, 89, 92, 95]
    _MAX_FILE_SIZE = 50000

    def __init__(self, original_image, output_dir):
        """Initalized the processor.

        Args:
            work_dir (str): directory where the output will be written.
            image_sizes (List[Tuple(int, int)]): list of width and height of the output images.
            qualities (List[int]): list of qualities.
        """
        self._original_image = original_image
        self._work_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self._QUALITIES.reverse()

    def Generate(self, image_sizes, qualities):
        for width, height in image_sizes:
            for quality in qualities:
                self.CreateImage(quality, width, height)

    def GenerateNative(self, image_sizes, qualities):
        for width, height in image_sizes:
            for quality in qualities:
             self.CreateImageNative(quality, width, height)

    def GetImageInfo(self, path):
        command = [self._IDENTIFY_COMMAND, '-format', '"%b %w %h"']
        command.append(path)
        print ' '.join(command), '->',
        output = subprocess.check_output(command)
        print output
        size_string, width, height = output.strip('" \n').split()
        return int(width), int(height), int(size_string[:-1])

    def CompressImage(self, quality, width, height):
        file_name = '%d-%d-%d.jpg' % (width, height, quality)
        output_file = os.path.join(self._work_dir, file_name)
        print 'generating %s...' % output_file
        image = Image(self._original_image)
        if not image.size.width == width:
            image.transform('%dx%d' %(width, height))
        image.quality(quality)
        image.write(output_file)
        return output_file

    def CompressImageNative(self, quality, width, height):
        original_file_name = os.path.split(self._original_image)[1].split('.')[0]
        extension = os.path.splitext(self._original_image)[1]
        file_name = '%s-%d-%d-%d%s' % (original_file_name, width, height, quality, extension)
        output_file = os.path.join(self._work_dir, file_name)
        command = [self._CONVERT_COMMAND, '-strip', '-interlace', 'Plane', '-quality']
        command.append('%d%%' % quality)
        command.append('-size')
        command.append('%dx%d' % (width, height))
        command.append(self._original_image)
        command.append(output_file)
        print ' '.join(command)
        subprocess.call(command)
        return output_file

    def AutoCompress(self, width, height):
        original_width, original_height, size = self.GetImageInfo(self._original_image)
        if size < self._MAX_FILE_SIZE or original_width < width or original_height < height:
            return None
        for quality in self._QUALITIES:
            output_file = self.CompressImageNative(quality, width, height)
            _, _, size = self.GetImageInfo(output_file)
            if size < self._MAX_FILE_SIZE:
                return output_file
            else:
                os.remove(output_file)

def BatchCompress(path):
    def visit(arg, dirname, names):
        for name in names:
            parts = os.path.splitext(name)
            if len(parts) != 2 or parts[1].lower() != '.jpg':
                continue
            file_path = os.path.join(dirname, name)
            output_dir = os.path.join(dirname, 'compressed')
            processor =  ImageProcessor(file_path, output_dir)
            output = processor.AutoCompress(450, 300)
            print 'selected ', output
            if output:
                shutil.copy(output, file_path)
    os.path.walk(path, visit, None)


def main():
    BatchCompress('../images')



if __name__ == '__main__':
    main()