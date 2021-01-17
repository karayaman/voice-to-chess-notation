import speech_recognition as sr
from pynput.keyboard import Key, Controller

import pickle
import numpy as np
from keras.models import load_model

filename = 'machinelearning.bin'
infile = open(filename, 'rb')
decode_dict, encode_next_value, encode_dict, max_len_x = pickle.load(infile)
infile.close()
model = load_model("my_model")


def one_hot_encode(row, max_len):
    row = "".join(c for c in row if c in encode_dict)
    encoding = np.zeros((1, max_len, encode_next_value), dtype=np.bool)
    for i, c in enumerate(row):
        v = encode_dict[c]
        encoding[0][i][v] = 1
    for i in range(len(row), max_len):  # padding
        v = 0
        encoding[0][i][v] = 1
    return encoding


def one_hot_decode(x):
    return ''.join(decode_dict[c] for c in x if c != 0)


r = sr.Recognizer()
keyboard = Controller()
commands = {"play": "play", "cancel": "cancel"}


def convert_to_notation(response):
    for alternative in response["alternative"]:
        phrase = alternative["transcript"]
        phrase = phrase.lower()
        if phrase in commands:
            return commands[phrase]

    for alternative in response["alternative"]:
        phrase = alternative["transcript"]
        phrase = phrase.lower()
        phrase = "".join(c for c in phrase if c.isalnum())
        if len(phrase) > max_len_x:
            phrase = phrase[:max_len_x]
        phrase = one_hot_encode(phrase, max_len_x)
        preds = model.predict_classes(phrase, verbose=0)
        notation = one_hot_decode(preds[0])
        return notation


phrase_time_limit = 5

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        try:
            state = "SPEAK!"
            print(state)
            audio = r.listen(source, phrase_time_limit=phrase_time_limit)
            response = r.recognize_google(audio, language="en-US", show_all=True)
            print(response)
            if not response:
                continue
            c = convert_to_notation(response)
            if c == "play":
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            elif c == "cancel":
                for _ in range(5):
                    keyboard.press(Key.backspace)
                    keyboard.release(Key.backspace)
            else:
                keyboard.type(c)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")
        except sr.WaitTimeoutError:
            print("Wait time out")
