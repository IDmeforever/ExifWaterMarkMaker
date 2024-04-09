import os
from datetime import datetime
from fractions import Fraction

import PIL
import exiftool
import image_to_numpy
from PIL import Image, ImageDraw, ImageFont, ExifTags
from PIL.ExifTags import TAGS

from ui.ui_helper import UIHelper

temp_img_path = "G:/Photos/2024/04/P1022795.JPG"
temp_img_path_fuji = "G:/Photos/103_FUJI/DSCF3001.JPG"
temp_img_path_vertical = "G:/Photos/2024/04/P1022797.JPG"
temp_img_small = "C:/Users/zhang/Desktop/202404/P1022560.JPG"

# 竖向增加的高度百分比, 百分数
white_vertical_percentage = 0.13


def is_file_image(file_path):
    """
    判断文件是否是图像
    :param file_path: 文件路径
    :return:
    """
    if not os.path.exists(file_path):
        return False
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError) as e:
        return False


def write_image_into_file(image, new_file_name, new_file_path=None):
    """
    保存Image对象到文件
    :param image: PIL.Image对象
    :param new_file_name: 目标文件名
    :param new_file_path: 目标保存路径, 可以不传
    :return:
    """
    new_path = os.path.join(os.getcwd(), new_file_name) if new_file_path is None else os.path.join(new_file_path,new_file_name)
    image.save(new_path, "JPEG", quality=95)
    print("Saved image file: {}".format(new_path))


def get_image_info_from_exif(image_path):
    """
    读取图片参数
    :param image_path: 图片路径
    :return: 参数信息词典
    """
    image = Image.open(image_path)
    exif = {PIL.ExifTags.TAGS[k]: v for k, v in image._getexif().items() if k in PIL.ExifTags.TAGS}
    # 读取镜头信息
    with exiftool.ExifToolHelper() as et:
        meta_dict = et.get_metadata(image_path)[0]
    lens_type = None
    if meta_dict.get("MakerNotes:LensType") is not None:
        lens_type = meta_dict.get("MakerNotes:LensType")
    elif meta_dict.get("MakerNotes:LensModel") is not None:
        lens_type = meta_dict.get("MakerNotes:LensModel")
    elif meta_dict.get("EXIF:LensType") is not None:
        lens_type = meta_dict.get("EXIF:LensType")
    elif meta_dict.get("EXIF:LensModel") is not None:
        lens_type = meta_dict.get("EXIF:LensModel")
    # 返回图片参数dict
    info_dict = {
        "make": str(exif.get("Make")),  # 相机厂商
        "model": str(exif.get("Model")),  # 相机型号
        "date": str(datetime.strptime(exif.get("DateTime"), "%Y:%m:%d %H:%M:%S")),  # 拍摄时间
        "focal_length": "{}mm".format(int(exif.get("FocalLength"))),  # 焦距
        "aperture": "F{}".format(exif.get("FNumber")),  # 光圈
        "iso": "ISO{}".format(exif.get("ISOSpeedRatings")),  # ISO
        "exposure_time": "{}s".format(Fraction(exif.get("ExposureTime").numerator, exif.get("ExposureTime").denominator)),  # 快门
        "lens_type": str(lens_type),  # 镜头
    }
    print(info_dict)
    return info_dict


def get_raw_rotation_img(file_path):
    """
    PIL读取带有exif的图像, 会自动旋转. 这里做旋转的矫正
    :param file_path: 图像路径
    :return: 旋转后的图像Image对象
    """
    image = Image.open(file_path)
    index = 0
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            index = orientation
            break
    exif = dict(image._getexif().items())
    if exif[index] == 3:
        image = image.rotate(180, expand=True)
    elif exif[index] == 6:
        image = image.rotate(270, expand=True)
    elif exif[index] == 8:
        image = image.rotate(90, expand=True)
    return image


def generate_space_area_img(file_path, exif_dict):
    """
    生成带有底部空白的图片对象
    :param file_path:
    :return:
    """
    if not is_file_image(file_path):
        print("This file path is not an image, please check whether the image exists.")
        return None
    origin_img = get_raw_rotation_img(file_path)
    width, height = origin_img.size
    print("origin_img size: ({}, {})".format(width, height))
    is_landscape = True if width > height else False  # 图片是否是横屏的
    # 底部白色bar的宽高
    white_width = int(width)
    white_height = int(height * white_vertical_percentage)
    # 生成各种ui配置
    ui_helper = UIHelper((white_width, white_height), is_landscape)

    # 创建底部的白色bar
    img_white_bar = Image.new('RGB', size=(white_width, white_height), color=(255, 255, 255))
    img_white_bar_draw = ImageDraw.Draw(img_white_bar)

    # 相机名称
    img_white_bar_draw.text(
        xy=ui_helper.get_element_padding("camera_name"),
        text="{} {}".format(exif_dict.get("make"), exif_dict.get("model")),
        fill=ui_helper.get_color("camera_name"),
        font=ui_helper.get_font("camera_name")
    )
    # 镜头名称
    img_white_bar_draw.text(
        xy=ui_helper.get_element_padding("lens_name"),
        text=exif_dict.get("lens_type"),
        fill=ui_helper.get_color("lens_name"),
        font=ui_helper.get_font("lens_name")
    )
    # 焦距 光圈 快门 ISO
    photo_param_content = "{} {} {} {}".format(exif_dict.get("focal_length"), exif_dict.get("aperture"), exif_dict.get("exposure_time"), exif_dict.get("iso"))
    photo_param_measure_width = img_white_bar_draw.textlength(photo_param_content, font=ui_helper.get_font("photo_param"))
    photo_param_x = width - ui_helper.get_element_padding("photo_param")[0] - photo_param_measure_width
    photo_param_y = ui_helper.get_element_padding("photo_param")[1]
    img_white_bar_draw.text(
        xy=(photo_param_x, photo_param_y),
        text=photo_param_content,
        fill=ui_helper.get_color("photo_param"),
        font=ui_helper.get_font("photo_param")
    )
    # 时间
    time_content = exif_dict.get("date")
    img_white_bar_draw.text(
        xy=(photo_param_x, ui_helper.get_element_padding("date")[1]),
        text=time_content,
        fill=ui_helper.get_color("date"),
        font=ui_helper.get_font("date")
    )
    # 画竖线
    line_x = (photo_param_x - int(white_width * 0.0133))
    line_y_start = int(white_height * 0.154)
    line_y_end = int(white_height * (1 - 0.154))
    img_white_bar_draw.line(
        (line_x, line_y_start, line_x, line_y_end),
        fill=(212, 212, 212),
        width=int(white_height * 0.008)
    )
    # 画logo
    logo_img = ui_helper.get_logo_img(exif_dict.get("make"))
    logo_width, logo_height = logo_img.size
    logo_x = int(line_x - white_width * 0.0133 - logo_width)
    logo_y = int((white_height - logo_height) / 2)
    img_white_bar.paste(logo_img, (logo_x, logo_y, logo_x + logo_width, logo_y + logo_height), logo_img)

    # 测试写文件
    write_image_into_file(img_white_bar, "test.jpg")


if __name__ == '__main__':
    generate_space_area_img(temp_img_small, get_image_info_from_exif(temp_img_small))

