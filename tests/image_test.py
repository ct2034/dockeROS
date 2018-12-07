#!/usr/bin/env python
PKG = 'dockeros'
from dockeros.image import DockeROSImage

import sys
import unittest
import docker

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
        self.assertEquals(1, 0, "1!=1")


if __name__ == '__main__':
    import rostest
    rostest.rosrun(PKG, 'test_lib', TestLib)
    rostest.rosrun(PKG, 'test_cli', TestCLI)
