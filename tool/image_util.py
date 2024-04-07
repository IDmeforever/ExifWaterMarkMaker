import os
from datetime import datetime
from fractions import Fraction

import PIL
import exiftool
from PIL import Image
from PIL.ExifTags import TAGS

temp_img_path = "G:/Photos/2024/04/P1022795.JPG"
temp_img_path_fuji = "G:/Photos/103_FUJI/DSCF3001.JPG"

# 竖向增加的高度百分比, 百分数
white_vertical_percentage = 13


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


def generate_new_img_with_space(file_path):
    """
    生成带有底部空白的图片对象
    :param file_path:
    :return:
    """
    if not is_file_image(file_path):
        print("This file path is not an image, please check whether the image exists.")
        return None
    origin_img = Image.open(file_path)
    width, height = origin_img.size
    is_landscape = True if width > height else False  # 图片是否是横屏的


if __name__ == '__main__':
    generate_new_img_with_space(temp_img_path)
    get_image_info_from_exif(temp_img_path)
