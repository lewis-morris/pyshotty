import io
import os
import random
import subprocess
import tempfile
import time
import urllib
from multiprocessing import Process, Pipe

from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

class Firefox:

    def __init__(self, browser_size=(1200, 630), browser_loc=None, driver_loc=None, save_path=None,
                 file_prefix="tempscreenshot_", randomise_filename=True):
        """

        :param save_path:
        :param url: Url to navigate to
        :param browser_loc: Firefox browser binary if not in PATH, if left as None checks for binary with "which firefox"
        :param driver_loc: geckodriver browser binary if not in PATH , if left as None checks for binary with "which geckodriver"
        :param file_prefix: the prefix of the file that is saved
        :param randomise_filename: BOOL - toggle off if you want static filenames
        :param browser_size: TUPLE (width,height) essentially size of the screenshot size
                             None - will leave the default size
        """

        self.base_path = save_path if save_path else tempfile.gettempdir()

        self._check_paths()

        self.filename = self.base_path + f"/{file_prefix}{random.randint(1, 1000000000) if randomise_filename else ''}.png"

        self.firefox_location = browser_loc
        self.geckodriver_location = driver_loc

        self.options = None

        self._set_up_browser(browser_size)

    def _check_paths(self):
        if not os.path.isdir(self.base_path):
            raise Exception("Save path not found")


    def _set_up_browser(self, browser_size):

        # check binaries exist
        if not self._firefox_exists():
            raise Exception("Firefox not found, possibly run 'sudo apt-get install firefox' in terminal")

        if not self._geckodriver_exists():
            raise Exception(
                "geckodriver not found, possibly run 'sudo apt-get install firefox-geckodriver' in terminal")

        # set up browser
        self.options = Options()
        self.options.headless = True

        if len(browser_size) == 2:
            if browser_size[0] < 450:
                raise Exception("Browser size must be larger than 450px")
            try:
                self.options.add_argument(f"--width={int(browser_size[0])}")
                self.options.add_argument(f"--height={int(browser_size[1])+85}")
            except ValueError:
                raise Exception("Browser size is not a valid number")
        elif browser_size:
            raise Exception("The browser size supplied is invalid")

    @staticmethod
    def _get_terminal_output(command, params):
        """Find location of binaries"""
        cmd = [command, params]
        res = subprocess.run(cmd, capture_output=True, shell=True)
        return res.stdout.decode().replace("\n","")

    def _firefox_exists(self):
        """
        Checks to see if it can find firefox or if path is user supplied, if the file exists
        """
        if self.firefox_location:
            return os.path.isfile(self.firefox_location)
        else:
            self.firefox_location = self._get_terminal_output("which firefox", "")
            return not self.firefox_location == ""

    def _geckodriver_exists(self):
        """
        Checks to see if it can find geckodriver or if path is user supplied, if the file exists
        """
        if self.geckodriver_location:
            return os.path.isfile(self.geckodriver_location)
        else:
            self.geckodriver_location = self._get_terminal_output("which geckodriver", "")
            return not self.geckodriver_location == ""

    def grab(self, url, wait_after_load=0, ret_type="png"):
        """
        Use to grab screenshot

        :param url: URL to grab
        :param wait_after_load: seconds of delay after page load before grabbing screen
        :param ret_type: what to return, options
                "png":saves image as png
                "jpg": saves image as jpg
                "pil": returns pil image

        :return: filename of screenshot

        """

        try:

            driver = webdriver.Firefox(options=self.options, firefox_binary=FirefoxBinary(self.firefox_location),
                                       executable_path=self.geckodriver_location)

            url = urllib.parse.unquote_plus(url)

            url = url.replace("www.", "")

            driver.get(url if "http" in url else "https://" + url)

            while True:
                x = driver.execute_script("return document.readyState")
                if x == "complete":
                    break

            time.sleep(wait_after_load)

            img = Image.open(io.BytesIO(driver.get_screenshot_as_png()))

            driver.close()

            if ret_type == "png":
                img.save(self.filename)
                return self.filename
            elif ret_type == "jpg":
                file = self.filename.replace(".png",".jpg")
                img.convert('RGB').save(file, "JPEG", quality=100)
                return file
            elif ret_type == "pil":
                return img
            else:
                raise Exception("format not found, please use one in [png,jpg,pil]")

        except Exception as e:

            return e