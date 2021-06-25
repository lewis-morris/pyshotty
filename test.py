from pyshotty import Firefox
screen = Firefox()
img = screen.grab("www.google.com", ret_type="jpg")
print(img)