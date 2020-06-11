#!/usr/bin/python
#
import jetson.inference
import jetson.utils

import argparse
import sys

# parse the command line
parser = argparse.ArgumentParser(description="Classify a live camera stream using an image recognition DNN.", 
						   formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.imageNet.Usage())

parser.add_argument("--network", type=str, default="googlenet", help="pre-trained model to load (see below for options)")
parser.add_argument("--camera", type=str, default="0", help="index of the MIPI CSI camera to use (e.g. CSI camera 0)\nor for VL42 cameras, the /dev/video device to use.\nby default, MIPI CSI camera 0 will be used.")
parser.add_argument("--width", type=int, default=1280, help="desired width of camera stream (default is 1280 pixels)")
parser.add_argument("--height", type=int, default=720, help="desired height of camera stream (default is 720 pixels)")

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the recognition network
net = jetson.inference.imageNet(opt.network, sys.argv)

# create the camera and display
font = jetson.utils.cudaFont()
camera = jetson.utils.gstCamera(opt.width, opt.height, opt.camera)
display = jetson.utils.glDisplay()

# initialize OLED ssd1306
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import to_japanese_ilsvrc2012
translator = to_japanese_ilsvrc2012.Ilsvrc2012Japanese()

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)
font2 = ImageFont.truetype('usr/share/fonts/truetype/fonts-japanese-gothic.ttf', 14)

# process frames until user exits
while display.IsOpen():
  # capture the image
  img, width, height = camera.CaptureRGBA()

  # classify the image
  class_idx, confidence = net.Classify(img, width, height)

  # find the object description
  class_desc = net.GetClassDesc(class_idx)

  # overlay the result on the image	
  font.OverlayText(img, width, height, "{:05.2f}% {:s}".format(confidence * 100, class_desc), 5, 5, font.White, font.Gray40)
	
  # render the image
  display.RenderOnce(img, width, height)

  # update the title bar
  display.SetTitle("{:s} | Network {:.0f} FPS".format(net.GetNetworkName(), net.GetNetworkFPS()))

  # print out performance info
  net.PrintProfilerTimes()

  # print the result on OLED ssd1306
  draw.rectangle((0, 0, width, height), outline=0, fill=0)
  draw.text((0, 0), "分類: " + translator.convert(class_desc), font=font2, fill=255)
  draw.text((0, 14), "確率: " + "{:0.2f}%".format(confidence * 100), font=font2, fill=255)
  disp.image(image)
  disp.show()

