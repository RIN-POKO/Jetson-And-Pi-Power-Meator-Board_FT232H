# -*- coding: utf-8 -*-
import os
os.environ['BLINKA_FT232H'] = '1'  # 環境変数の設定
import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

import board
import adafruit_ina260
i2c2 = board.I2C()
ina260 = adafruit_ina260.INA260(i2c2)

while True:
  c = ina260.current
  v = ina260.voltage
  p = ina260.power
  print("Current: %.2f Voltage: %.2f Power: %.2f" %(c, v, p))

  # Draw a black filled box to clear the image.
  draw.rectangle((0, 0, width, height), outline=0, fill=0)

  # Write four lines of text.
  draw.text((x, top + 0), "Current(mA): " + str("{0:.2f}".format(c)) + '     ', font=font, fill=255)
  draw.text((x, top + 14), "Voltage(V): " + str("{0:.2f}".format(v)) + '     ', font=font, fill=255)
  draw.text((x, top + 28), "Power(mW): " + str("{0:.2f}".format(p)) + '     ', font=font, fill=255)

  # Display image.
  disp.image(image)
  disp.show()
  time.sleep(1)

