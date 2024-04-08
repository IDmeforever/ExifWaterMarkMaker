from PIL import ImageFont

# 字体路径
normal_font_path = "../assets/fonts/MiSans.ttf"
bold_font_path = "../assets/fonts/MiSans-Bold.ttf"


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
        # todo 横竖屏适配
        if scene == "camera_name":  # 相机名称
            return self.area_height * 0.18
        if scene == "lens_name":  # 镜头型号
            return self.area_height * 0.154
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
        if scene == "camera_name":
            return int(self.area_width * 0.05), int(self.area_height * 0.268)
        if scene == "lens_name":
            return int(self.area_width * 0.05), int(self.area_height * 0.560)
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
        return 0, 0, 0
