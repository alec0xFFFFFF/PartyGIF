from change_hue import create_shifted_hue_images
from make_gif import create_gif, write_gif
import os
import magic
from PIL import Image, ImageDraw, ImageFont
import textwrap
from math import ceil
import zipfile


def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def create_party_gif(input_image, output_name):
    output_dir = 'temp_output'
    create_shifted_hue_images(input_image, output_dir)
    create_gif(output_name, output_dir)


def create_text_image(text_image_path, msg, image_width, image_height):
    # todo get/set right ratio of image size to font and padding for wrap text width
    font = ImageFont.truetype('/Library/Fonts/Androgyne_TB.otf', 40)
    msg_lines = textwrap.wrap(msg, width=30)
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(msg)
    img = Image.new('RGB', (image_width, image_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    current_h, pad = (image_height - ((ascent - offset_y) * msg_lines.__len__())) / 2, 10
    for line in msg_lines:
        w, h = draw.textsize(line, font=font)

        draw.text(((image_width - w) / 2, current_h), line, font=font, fill=(255, 255, 255))
        current_h += h + pad
    img.save(text_image_path)


def resize_and_center_image_in_frame(output_image_path, input_image_path, width, height):
    image = Image.open(input_image_path)
    im_new = expand2square(image, (255, 255, 255)).resize((width, height))
    im_new.save(output_image_path)


def create_scroller_image(output_image_path, output_images, width):
    height = width*output_images.__len__()
    long_image = Image.new('RGB', (width, height), color=(0, 0, 0))
    for i, im_path in enumerate(output_images):
        im = Image.open(im_path)
        position = (0, width*i)
        long_image.paste(im, position)
    long_image.save(output_image_path)


def create_all_view_image(output_image_path, output_images, single_image_width, numbered_labels=True):
    # add numbers
    if output_images.__len__() % 2 == 1:
        width = ceil((output_images.__len__() + 1) * single_image_width / 2)
        # what to put in end square?
    else:
        width = ceil(output_images.__len__() * single_image_width / 2)
    height = single_image_width * 2
    sideways_image = Image.new('RGB', (width, height), color=(0, 0, 0))
    x = 0
    for i, im_path in enumerate(output_images):
        im = Image.open(im_path)
        paste_top_left_coordinates = (single_image_width * x, (i % 2) * single_image_width)
        sideways_image.paste(im, paste_top_left_coordinates)

        # draw number label
        if i > 0 and numbered_labels:
            draw = ImageDraw.Draw(sideways_image)
            # (x1, y1, x2, y2)
            offset = 10
            diameter = 70
            draw_circle_coordinates = ((single_image_width * x) + offset, ((i % 2) * single_image_width) + offset,
                                       (single_image_width * x) + (offset + diameter), ((i % 2) * single_image_width) + (offset + diameter))

            num = str(i)
            draw.ellipse(draw_circle_coordinates, outline='red', fill='red')
            font = ImageFont.truetype('/Library/Fonts/TitilliumWeb-Bold.ttf', 40)
            ascent, descent = font.getmetrics()
            (text_width, baseline), (offset_x, offset_y) = font.font.getsize(num)
            # todo fix centering of text in circle
            number_coordinate = ((single_image_width * x) + ((offset+diameter)/2)-(text_width/4), ((i % 2) * single_image_width) + ((offset+diameter)/2)-(28))
            draw.text(number_coordinate, num, font=font, fill='white')
        if (i % 2) == 1:
            x += 1
    sideways_image.save(output_image_path)


def get_ordered_responses(input_dir_path):
    """
    returns list of tuples of submission number, type, path, timestamp ordered by file name number
    ex. ('0', 'image/jpeg', '/Users/alexanderkwhite/Desktop/Telestrations/week 2/Items/06/0.jpg', 1589811365.8658662)
    :param input_dir_path:
    :return:
    """
    return sorted([(f.split('.', 1)[0], magic.from_file(os.path.join(input_dir_path, f), mime=True),
                    os.path.join(input_dir_path, f),
                    os.path.getmtime(os.path.join(input_dir_path, f))) for f in os.listdir(input_dir_path)
                   if (os.path.isfile(os.path.join(input_dir_path, f))
                        and (magic.from_file(os.path.join(input_dir_path, f), mime=True)[:4] == 'text'
                             or magic.from_file(os.path.join(input_dir_path, f), mime=True)[:5] == 'image'))],
                  key=lambda x: x[0])


def get_ordered_tasks(input_dir_path):
    return sorted([(os.path.join(input_dir_path, f), f) for f in os.listdir(input_dir_path) if
                   os.path.isdir(os.path.join(input_dir_path, f))], key=lambda x: x[1])


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))


def create_result_medias(input_path, output_path, width, height):
    file_items = get_ordered_tasks(input_path)
    media_output_path = output_path+'/media'

    # todo temp files instead
    item_output_path = output_path + '/output'

    for res_dir_file_path, i in file_items:
        files = get_ordered_responses(res_dir_file_path)
        os.makedirs(item_output_path, exist_ok=True)
        output_images = list()

        for j, submission in enumerate(files):
            if j == 0:
                # create_title card that is used with each gif
                with open(submission[2], 'rt') as text_file:
                    title_msg = 'The Gang Draws: {}'.format(text_file.read())
                title_card_path = '{}/title.png'.format(item_output_path)
                create_text_image(title_card_path, title_msg, width, height)
                output_images.append(title_card_path)
            else:
                if submission[1][:4] == 'text':
                    with open(submission[2], 'rt') as text_file:
                        # first one "the gang draws"
                        msg = text_file.read()
                    text_image_path = '{}/{}.png'.format(item_output_path, submission[0])
                    create_text_image(text_image_path, msg, width, height)
                    output_images.append(text_image_path)
                else:
                    output_image_path = '{}/{}.png'.format(item_output_path, submission[0])
                    resize_and_center_image_in_frame(output_image_path, submission[2], width, height)
                    output_images.append(output_image_path)

        os.makedirs(media_output_path, exist_ok=True)
        write_gif(output_images, '{}/{}_motion'.format(media_output_path, i), 3)

        create_scroller_image('{}/{}_scroller.png'.format(media_output_path, i), output_images, width)

        create_all_view_image('{}/{}_all_view.png'.format(media_output_path, i), output_images, width)

        # todo keep images in memory?
        # todo put names on images?
        # todo determine frame length based on amount of text and type?
        # todo font size according to image size
        # todo fix centering of circle
        # todo create gif with circle on images
        # todo make a live photo version of this?
        # todo analyze phrases and make off the rail graphic
        # todo make gif of all?
    # zip all at end in the media output path
    with zipfile.ZipFile('{}/week_2_results.zip'.format(output_path), 'w', zipfile.ZIP_DEFLATED) as z:
        zipdir(media_output_path, z)


if __name__ == '__main__':
    # input_file = 'assets/gator.png'
    # output = 'assets/gator.gif'
    # create_party_gif(input_file, output)

    week_2_input_path = r'/Users/alexanderkwhite/Desktop/Telestrations/week 2/Items'

    week_2_output_path = r'/Users/alexanderkwhite/PycharmProjects/PartyGIF/week_2'

    create_result_medias(week_2_input_path, week_2_output_path, 800, 800)
