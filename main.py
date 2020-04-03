from change_hue import create_shifted_hue_images
from make_gif import create_gif


def create_party_gif(input_image, output_name):
    output_dir = 'temp_output'
    create_shifted_hue_images(input_image, output_dir)
    create_gif(output_name, output_dir)


if __name__ == '__main__':
    input_file = 'assets/gator.png'
    output = 'assets/gator.gif'
    create_party_gif(input_file, output)
