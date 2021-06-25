import os
import random
import subprocess
import tempfile
import urllib
from multiprocessing import Process, Pipe
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

class Firefox:

    def __init__(self, url, browser_loc=None, driver_loc=None, randomise_filename=True, browser_size=(1200, 630)):
        """

        :param url: Url to navigate to
        :param browser_loc: Firefox browser binary if not in PATH, if left as None checks for binary with "which firefox"
        :param driver_loc: geckodriver browser binary if not in PATH , if left as None checks for binary with "which geckodriver"
        :param randomise_filename: BOOL - toggle off if you want static filenames
        :param browser_size: TUPLE (width,height) essentially size of the screenshot size
                             None - will leave the default size
        """

        self.url = url
        self.filename = tempfile.gettempdir() + f"/tempscreenshot_{random.randint(1, 1000000000) if randomise_filename else ''}.png"
        self.parent_conn = None
        self.firefox_location = browser_loc
        self.geckodriver_location = driver_loc
        self.options = None
        self._set_up_browser(browser_size)

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
            try:
                self.options.add_argument(f"--width={int(browser_size[0])}")
                self.options.add_argument(f"--height={int(browser_size[1])}")
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

    def run(self):
        """
        Use to grab screenshot
        :return: filename of screenshot
        """
        # creates the communinication between processes
        self.parent_conn, child_conn = Pipe()
        # loads the process
        process = Process(target=self._get_screenshot, args=[child_conn])
        # start the process
        process.daemon = True
        process.start()

        # wait for process completion.
        while True:
            out = self.parent_conn.recv()
            if out and out == 1:
                return self.filename
            elif out:
                raise Exception(out)

    def _get_screenshot(self, child_conn):
        """
        saves screenshot as a process
        :param child_conn: Pipe for communication between parent and child process.
        :return: screenshot file name
        """
        try:

            driver = webdriver.Firefox(options=self.options, firefox_binary=FirefoxBinary(self.firefox_location),
                                       executable_path=self.geckodriver_location)

            url = urllib.parse.unquote_plus(self.url)

            driver.get(url if "http" in url else "https://" + url)

            while True:
                x = driver.execute_script("return document.readyState")
                if x == "complete":
                    break

            driver.save_screenshot(self.filename)

            driver.close()
            child_conn.send(1)

        except Exception as e:

            child_conn.send(e)