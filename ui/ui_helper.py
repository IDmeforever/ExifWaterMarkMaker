# -*- coding: utf-8 -*-
import os

from tool.logo_util import get_logo_file_path
from PIL import Image, ImageFont
from PIL.Image import Resampling

file_dir = os.path.dirname(__file__)

# 字体路径
normal_font_path = os.path.join(file_dir, "../assets/fonts/MiSans.ttf")
bold_font_path = os.path.join(file_dir, "../assets/fonts/MiSans-Bold.ttf")

# 竖屏字体缩放系数
vertical_resize_factor = 0.85

# Logo最大尺寸
logo_max_width_landscape = 40
logo_max_height_landscape = 30
logo_max_width_vertical = 60
logo_max_height_vertical = 45
landscape_logo_height_ratio = 52 / 600
vertical_logo_height_ratio = 60 / 600

class UIHelper:
    def __init__(self, _area_size, _is_landscape):
        self.area_width, self.area_height = _area_size
        self.is_landscape = _is_landscape

    def get_font_size(self, scene):
        """
        获取不同场景字体的大小
        :param scene: 场景
        :return: 字体大小
        """
        if self.is_landscape:
            # 横屏模式
            if scene == "camera_name":  # 相机名称
                return self.area_height * 0.18
            if scene == "lens_name":  # 镜头型号
                return self.area_height * 0.154
            if scene == "photo_param":  # 图片参数
                return self.area_height * 0.18
            if scene == "date":  # 日期
                return self.area_height * 0.154
        else:
            # 竖屏参数
            if scene == "camera_name":  # 相机名称
                return self.area_height * 0.18 * vertical_resize_factor
            if scene == "lens_name":  # 镜头型号
                return self.area_height * 0.154 * vertical_resize_factor
            if scene == "photo_param":  # 图片参数
                return self.area_height * 0.18 * vertical_resize_factor
            if scene == "date":  # 日期
                return self.area_height * 0.154 * vertical_resize_factor
        return 50

    def get_font(self, scene):
        """
        获取ImageFont字体对象
        :param scene: 场景
        :return: 对应的ImageFont字体对象
        """
        final_bold = True
        if scene == "lens_name":
            final_bold = False
        elif scene == "date":
            final_bold = False

        if final_bold:
            return ImageFont.truetype(bold_font_path, self.get_font_size(scene))
        else:
            return ImageFont.truetype(normal_font_path, self.get_font_size(scene))

    def get_element_padding(self, scene):
        """
        获取元素对应左上角的padding
        :param scene: 元素名
        :return:
        """
        ratio = 1 if self.is_landscape else vertical_resize_factor
        if scene == "camera_name":
            return int(self.area_width * 0.05 * ratio), int(self.area_height * 0.268)
        if scene == "lens_name":
            return int(self.area_width * 0.05 * ratio), int(self.area_height * 0.560)
        if scene == "photo_param":
            return int(self.area_width * 0.05 * ratio), int(self.area_height * 0.268)
        if scene == "date":
            return int(self.area_width * 0.05 * ratio), int(self.area_height * 0.560)
        return 0, 0

    def get_color(self, scene):
        """
        获取文字颜色
        :param scene: 场景
        :return: 颜色的三元组
        """
        if scene == "camera_name":
            return 0, 0, 0
        elif scene == "lens_name":
            return 133, 133, 133
        elif scene == "photo_param":
            return 0, 0, 0
        elif scene == "date":
            return 133, 133, 133
        return 0, 0, 0

    def get_logo_img(self, company):
        """
        获取Logo Image对象，最长不超过(40/600)*width, 最高不超过(30/52)*height
        :param company: 厂商名
        :return:
        """
        logo_path = get_logo_file_path(company)
        if logo_path is None:
            print("unsupported company logo: {}".format(company))
            return None
        logo_img = Image.open(logo_path)
        logo_width, logo_height = logo_img.size
        width_base = 600
        height_base = 52 if self.is_landscape else 60
        max_width = logo_max_width_landscape if self.is_landscape else logo_max_width_vertical
        max_height = logo_max_height_landscape if self.is_landscape else logo_max_height_vertical
        # 谁长就先按谁缩放
        if logo_width > logo_height:
            resize_width = (max_width / width_base) * self.area_width
            factor = resize_width / logo_width
            resize_height = logo_height * factor
            if resize_height > (max_height / height_base) * self.area_height:
                # 按高来缩放
                resize_height = (max_height / height_base) * self.area_height
                factor = resize_height / logo_height
                resize_width = logo_width * factor
        else:
            resize_height = (max_height / height_base) * self.area_height
            factor = resize_height / logo_height
            resize_width = logo_width * factor
            if resize_width > (max_width / width_base) * self.area_width:
                # 按宽来缩放
                resize_width = (max_width / width_base) * self.area_width
                factor = resize_width / logo_width
                resize_height = logo_height * factor
        # print("resize to {} {}".format(resize_width, resize_height))
        resize_img = logo_img.resize((int(resize_width), int(resize_height)), resample=Resampling.LANCZOS)
        return resize_img
