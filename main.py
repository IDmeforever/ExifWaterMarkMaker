import sys

from tool.image_util import get_image_info_from_exif, generate_space_area_img, output_img_with_info_bar

if __name__ == '__main__':
    args = sys.argv[1:]
    if args is not None and len(args) >= 1:
        print("files list: {}".format(args))
        for arg in args:
            image_exif_info = get_image_info_from_exif(arg)
            bar_img = generate_space_area_img(arg, image_exif_info)
            output_img_with_info_bar(arg, bar_img)
    else:
        print("Please drag and drop the image onto the script, or enter the list of files when executing the command from the command line.")
    # 任意按键以退出
    input("Press any button to exit...")
