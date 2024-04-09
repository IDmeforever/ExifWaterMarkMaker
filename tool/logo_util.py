import os.path

# 定义厂商和对应的logo文件
logo_dict = {
    "canon": os.path.abspath("../assets/logo/canon.png"),
    "fujifilm": os.path.abspath("../assets/logo/fujifilm.png"),
    "hasselblad": os.path.abspath("../assets/logo/hasselblad.png"),
    "leica": os.path.abspath("../assets/logo/leica.png"),
    "nikon": os.path.abspath("../assets/logo/nikon.png"),
    "panasonic": os.path.abspath("../assets/logo/panasonic.png"),
    "sony": os.path.abspath("../assets/logo/sony.png")
}


def get_logo_file_path(company_name):
    """
    输入厂商名称, 输出logo文件路径. 若不存在该图片, 则返回None.
    :param company_name: 厂商名称, 支持大小写
    :return: logo文件path
    """
    return logo_dict.get(company_name.lower())


if __name__ == '__main__':
    print(get_logo_file_path("panasonic"))
