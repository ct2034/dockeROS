from src.dockeros.image import DockeROSImage


def make_source_image_test():
    dri = DockeROSImage(["roslaunch", "my_pckg", "foo.launch"], {})
    dri.build_image()
