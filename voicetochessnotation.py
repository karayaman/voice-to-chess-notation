import speech_recognition as sr
from pynput.keyboard import Key, Controller

r = sr.Recognizer()
keyboard = Controller()
commands = {"one": "1", "two": "2", "three": "3",
            "four": "4", "five": "5", "six": "6", "seven": "7",
            "eight": "8", "nine": "9", "play": "play", "cancel": "cancel",
            "knight": "N", "night": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}


def convert_to_notation_helper(word):
    if word in commands:
        return commands[word]

    if word[0].isdigit():
        return word[0]

    if len(word) >= 2 and word[1].isdigit():
        return word[:2]
    return word[0]


def convert_to_notation(response):
    for alternative in response["alternative"]:
        phrase = alternative["transcript"]
        if phrase[0].isdigit():
            return phrase[0]

        if phrase in commands:
            return commands[phrase]

    for alternative in response["alternative"]:
        phrase = alternative["transcript"]
        words = phrase.split()
        return "".join(convert_to_notation_helper(word.lower()) for word in words)


timeout = 2
phrase_time_limit = 5

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        try:
            state = "SPEAK!"
            print(state)
            audio = r.listen(source, phrase_time_limit=phrase_time_limit)
            response = r.recognize_google(audio, language="en-EN", show_all=True)
            print(response)
            if not response:
                continue
            c = convert_to_notation(response)
            if c == "play":
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            elif c == "cancel":
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
