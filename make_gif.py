import imageio
from PIL import Image
from os import listdir
from os.path import isfile, join


def write_gif(filenames, output_name, frame_duration=1):
    # if not .gif on end change to that and inform user
    images = []
    if output_name[-4:] != '.gif':
        output_name += '.gif'
        print("Added gif extension to output file path: {}".format(output_name))
    for filename in filenames:
        try:
            img = Image.open(filename)  # open the image file
            img.verify()  # verify that it is, in fact an image
            images.append(imageio.imread(filename))
        except (IOError, SyntaxError) as e:
            print('Bad file:', filename)
    imageio.mimsave(output_name, images, format='GIF', duration=frame_duration)


def get_filenames(directory):
    return [directory + '/' + f for f in listdir(directory) if isfile(join(directory, f))]


def create_gif(output_name, input_dir, frame_duration=1):
    """

    :param output_name:
    :param input_dir:
    :param frame_duration: integer -- seconds frame should be displayed
    :return:
    """
    file_names = get_filenames(input_dir)
    write_gif(file_names, output_name, frame_duration)


if __name__ == '__main__':
    input_dir = 'output_jpegs'
    create_gif("movie.gif", input_dir)
