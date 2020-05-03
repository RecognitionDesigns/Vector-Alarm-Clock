#!/usr/bin/env python3

# Copyright (c) 2020 Recognition Designs Ltd, Colin Twigg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# for use with DDL/Anki's Vector Robot: https://www.anki.com/en-us/vector

import anki_vector
import time
import sys
from anki_vector.util import degrees
from anki_vector.events import Events
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, date

def make_text_image(text_to_draw, x, y, font=None):
    dimensions = (184, 96)
    text_image = Image.new('RGBA', dimensions, (0, 0, 0, 255))
    dc = ImageDraw.Draw(text_image)
    dc.text((x, y), text_to_draw, fill=(0, 255, 0, 255), font=font)
    return text_image

try:
    font_file = ImageFont.truetype("lcd.ttf", 75)
except IOError:
    try:
        font_file = ImageFont.truetype("arial.ttf", 27)
    except IOError:
        pass
    
import datetime
print(datetime.datetime.today().strftime("%H:%M"))
today = date.today()
if (today.weekday() == 0):
    print("Monday")
if (today.weekday() == 1):
    print("Tuesday")
if (today.weekday() == 2):
    print("Wednesday")
if (today.weekday() == 3):
    print("Thursday")
if (today.weekday() == 4):
    print("Friday")
if (today.weekday() == 5):
    print("Saturday")
if (today.weekday() == 6):
    print("Sunday")
#day=int(input("Enter a Day of the week number, 0=M 1=T 2=W 3=Th 4=F 5=F 6=Sn: "))
hour=int(input("Enter an Hour: "))
minute=int(input("Enter a Minute: "))
#hour=int(21)
#minute=int(46)
while True:
    if hour == int(datetime.datetime.today().strftime("%H")) and minute == int(datetime.datetime.today().strftime("%M")):
        print("Alarm Raised")
        
        with anki_vector.AsyncRobot() as robot:
            for x in range(0, 10):
                datetime.datetime.now().strftime(('%H:%M'))
            
                robot.anim.play_animation_trigger('GreetAfterLongTime')
                robot.audio.stream_wav_file("vector_alert.wav", 75).result()

                robot.behavior.set_head_angle(degrees(30.0))
                robot.behavior.set_lift_height(0.0)

                time1 = datetime.datetime.now().strftime(('%H:%M'))
                face_sum = (str(time1))
                text_to_draw = face_sum
                face_image = make_text_image(text_to_draw, 20, 5, font_file)
                args = anki_vector.util.parse_command_args()

                print("Display time on Vector's face...")
                screen_data = anki_vector.screen.convert_image_to_screen_data(face_image)
                robot.screen.set_screen_with_image_data(screen_data, 10.0, interrupt_running=True)

                action = robot.behavior.say_text("The time is {}".format(str(time1)))

                while True:

                    if action.done():
                            print("Alarm complete!")
                            break

                    if robot.touch.last_sensor_reading.is_being_touched:
                            print("Alarm Cancelled!")
                            sys.exit()
                            break

        break
    else:
        time.sleep(1)
