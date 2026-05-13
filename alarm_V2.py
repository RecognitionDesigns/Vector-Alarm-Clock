#!/usr/bin/env python3
# Copyright (c) 2020 Recognition Designs Ltd, Colin Twigg
# Licensed under the Apache License, Version 2.0

import sys
import time
import datetime
import calendar

import anki_vector
from anki_vector.util import degrees
from PIL import Image, ImageDraw, ImageFont

# --- Constants ---
SCREEN_W, SCREEN_H = 184, 96
AUDIO_VOLUME = 75
SCREEN_DURATION = 10.0
HEAD_ANGLE = 30.0
POLL_INTERVAL = 1  # seconds between alarm checks

# --- Font loading ---
def load_font():
    for font_name, size in [("lcd.ttf", 75), ("arial.ttf", 27)]:
        try:
            return ImageFont.truetype(font_name, size)
        except IOError:
            continue
    return ImageFont.load_default()  # fallback instead of crashing

FONT = load_font()

# --- Image helper ---
def make_time_image(time_str, font):
    img = Image.new('RGBA', (SCREEN_W, SCREEN_H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 5), time_str, fill=(0, 255, 0, 255), font=font)
    return img

# --- Input ---
def get_alarm_time():
    today = datetime.date.today()
    print(f"Today is {calendar.day_name[today.weekday()]}, {datetime.datetime.now().strftime('%H:%M')}")
    day = int(input("Enter day of week (0=Mon … 6=Sun): "))
    hour = int(input("Enter hour (0-23): "))
    minute = int(input("Enter minute (0-59): "))
    return day, hour, minute

# --- Alarm trigger ---
def trigger_alarm():
    try:
        with anki_vector.AsyncRobot() as robot:
            now_str = datetime.datetime.now().strftime('%H:%M')
            print(f"Alarm triggered at {now_str}")

            robot.anim.play_animation_trigger('GreetAfterLongTime')
            robot.audio.stream_wav_file("vector_alert.wav", AUDIO_VOLUME).result()
            robot.behavior.set_head_angle(degrees(HEAD_ANGLE))
            robot.behavior.set_lift_height(0.0)

            face_image = make_time_image(now_str, FONT)
            screen_data = anki_vector.screen.convert_image_to_screen_data(face_image)
            robot.screen.set_screen_with_image_data(screen_data, SCREEN_DURATION, interrupt_running=True)

            action = robot.behavior.say_text(f"The time is {now_str}")

            while not action.done():
                if robot.touch.last_sensor_reading.is_being_touched:
                    print("Alarm cancelled by touch.")
                    return
                time.sleep(0.1)

            print("Alarm complete!")

    except Exception as e:
        print(f"Error communicating with Vector: {e}")
        sys.exit(1)

# --- Main loop ---
def main():
    day, hour, minute = get_alarm_time()
    print("Waiting for alarm...")

    try:
        while True:
            now = datetime.datetime.now()
            today = datetime.date.today()
            if (today.weekday() == day
                    and now.hour == hour
                    and now.minute == minute):
                trigger_alarm()
                break
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nAlarm cancelled.")

if __name__ == "__main__":
    main()
