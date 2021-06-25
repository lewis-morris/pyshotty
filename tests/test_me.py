import unittest
import os
from PIL import Image

import PIL

import pyshotty

class MyTestCase(unittest.TestCase):

    def test_png(self):
        screen = pyshotty.Firefox()
        fl = screen.grab("www.google.com")
        self.assertTrue(os.path.isfile(fl))

    def test_jpg(self):
        screen = pyshotty.Firefox()
        fl = screen.grab("www.google.com", ret_type="jpg")
        self.assertTrue(fl.endswith(".jpg"))
        self.assertTrue(os.path.isfile(fl))

    def test_pil(self):
        screen = pyshotty.Firefox()
        fl = screen.grab("www.google.com", ret_type="pil")
        self.assertTrue(type(fl) == PIL.PngImagePlugin.PngImageFile)

    def test_size_change(self):
        screen = pyshotty.Firefox((2000, 2000))
        fl = screen.grab("www.google.com", ret_type="pil")

        self.assertTrue(fl.size[0] == 2000)
        self.assertTrue(fl.size[1] == 2000)

        screen = pyshotty.Firefox((450, 450))
        fl = screen.grab("www.google.com", ret_type="pil")

        self.assertTrue(fl.size[0] == 450)
        self.assertTrue(fl.size[1] == 450)

    def test_size_error(self):
        with self.assertRaises(Exception):
            screen = pyshotty.Firefox((300, 300))
            fl = screen.grab("www.google.com", ret_type="pil")
    def test_size_error2(self):
        with self.assertRaises(Exception):
            screen = pyshotty.Firefox(("ds", 300))
            fl = screen.grab("www.google.com", ret_type="pil")
    def test_patherror(self):
        with self.assertRaises(Exception):
            screen = pyshotty.Firefox(save_path="/sdasdas/")

    def test_set_firefox_path(self):
        screen = pyshotty.Firefox(browser_loc="/usr/bin/firefox")
        fl = screen.grab("www.google.com")
        self.assertTrue(os.path.isfile(fl))

    def test_set_driver_path(self):
        screen = pyshotty.Firefox(driver_loc="/usr/bin/geckodriver")
        fl = screen.grab("www.google.com")
        self.assertTrue(os.path.isfile(fl))

    def test_sleep(self):
        screen = pyshotty.Firefox(driver_loc="/usr/bin/geckodriver")
        fl = screen.grab("www.google.com", wait_after_load=2)
        self.assertTrue(os.path.isfile(fl))

    def test_firefox_path_error(self):
        with self.assertRaises(Exception):
            screen = pyshotty.Firefox(browser_loc="/usr/bin/firefoxd")
            fl = screen.grab("www.google.com")
            screen.driver.close()
            self.assertTrue(os.path.isfile(fl))

    def test_driver_path_error(self):
        with self.assertRaises(Exception):
            screen = pyshotty.Firefox(driver_loc="/usr/bin/geckodrsiver")
            fl = screen.grab("www.google.com")
            screen.driver.close()
            self.assertTrue(os.path.isfile(fl))


if __name__ == '__main__':
    unittest.main()
