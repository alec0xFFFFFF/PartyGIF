import imageio
from PIL import Image
from os import listdir
from os.path import isfile, join


def write_gif(filenames, output_name):
    images = []
    for filename in filenames:
        try:
            img = Image.open(filename)  # open the image file
            img.verify()  # verify that it is, in fact an image
            images.append(imageio.imread(filename))
        except (IOError, SyntaxError) as e:
            print('Bad file:', filename)
    imageio.mimsave(output_name, images)


def get_filenames(directory):
    return [directory + '/' + f for f in listdir(directory) if isfile(join(directory, f))]


def create_gif(output_name, input_dir):
    file_names = get_filenames(input_dir)
    write_gif(file_names, output_name)


if __name__ == '__main__':
    input_dir = 'output_jpegs'
    create_gif("movie.gif", input_dir)
