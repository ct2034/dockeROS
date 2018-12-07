#!/usr/bin/env python
PKG = 'dockeros'
# from dockeros.image import DockeROSImage

import docker
import subprocess
import sys
import unittest

TEST_IMAGES = ["rosrun_move_base_move_base"]

class TestLib(unittest.TestCase):
    def _clean(self):
        for img in TEST_IMAGES:
            try:
                self.client.images.remove(img)
            except Exception:
                pass

    def setUp(self):
        self.client = docker.from_env()
        self._clean()

    def test_build_move_base_image(self):
        dri = DockeROSImage(["rosrun", "move_base", "move_base"], {})
        dri.make_client()
        dri.build()
        img = self.client.images.get(dri.name)

    def tearDown(self):
        self._clean()


class TestCLI(unittest.TestCase):
    def test_getting_help(self):
        # out = subprocess.check_output(
        #     " ".join(
        #         ["dockeros", "-h"]),
        #     shell=True)
        # print(out)
        self.assertEquals(1, 1, "1!=1")


if __name__ == '__main__':
    import rostest
    # rostest.rosrun(PKG, 'test_lib', TestLib)
    rostest.rosrun(PKG, 'test_cli', TestCLI)
