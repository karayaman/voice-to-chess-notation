import pickle
import numpy as np
from keras.models import load_model
from chess import square_name
import speech_recognition as sr


class Voice_to_chess_notation:
    def __init__(self):
        filename = 'machinelearning.bin'
        infile = open(filename, 'rb')
        self.decode_dict, self.encode_next_value, self.encode_dict, self.max_len_x = pickle.load(infile)
        infile.close()
        self.model = load_model("my_model")
        self.r = sr.Recognizer()

    def one_hot_encode(self, row, max_len):
        row = "".join(c for c in row if c in self.encode_dict)
        encoding = np.zeros((1, max_len, self.encode_next_value), dtype=np.bool)
        for i, c in enumerate(row):
            v = self.encode_dict[c]
            encoding[0][i][v] = 1
        for i in range(len(row), max_len):  # padding
            v = 0
            encoding[0][i][v] = 1
        return encoding

    def one_hot_decode(self, x):
        return ''.join(self.decode_dict[c] for c in x)

    def convert_to_notation(self, response):
        notations = []
        for alternative in response["alternative"]:
            phrase = alternative["transcript"]
            phrase = phrase.lower()
            phrase = "".join(c for c in phrase if c.isalnum())
            if len(phrase) > self.max_len_x:
                phrase = phrase[:self.max_len_x]
            phrase = self.one_hot_encode(phrase, self.max_len_x)
            preds = self.model.predict_classes(phrase, verbose=0)
            notation = self.one_hot_decode(preds[0])
            notations.append(notation)
        return notations

    def listen(self):
        phrase_time_limit = 5

        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            while True:
                try:
                    state = "SPEAK!"
                    print(state)
                    audio = self.r.listen(source, phrase_time_limit=phrase_time_limit)
                    response = self.r.recognize_google(audio, language="en-US", show_all=True)
                    print(response)
                    if not response:
                        continue
                    return self.convert_to_notation(response)
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
                except sr.UnknownValueError:
                    print("unknown error occured")
                except sr.WaitTimeoutError:
                    print("Wait time out")

    def play(self, board):
        notations = self.listen()
        for notation in notations:
            start_piece, start_file, start_rank, end_file, end_rank = "P", "", "", "", ""
            for c in notation:
                if c.isupper():
                    start_piece = c
                elif c.islower():
                    if end_file:
                        start_file = end_file
                    end_file = c
                elif c.isdigit():
                    if end_rank:
                        start_rank = end_rank
                    end_rank = c

            moves = list(board.legal_moves)
            p_moves = [move for move in moves if board.piece_at(move.from_square).symbol().upper() == start_piece]
            if start_file:
                p_moves = [move for move in p_moves if square_name(move.from_square)[0] == start_file]
            if start_rank:
                p_moves = [move for move in p_moves if square_name(move.from_square)[1] == start_rank]
            r_moves = [move for move in p_moves if square_name(move.to_square)[1] == end_rank]
            f_moves = [move for move in r_moves if square_name(move.to_square)[0] == end_file]

            if not end_file:
                continue

            if not end_rank:
                continue

            if len(f_moves) == 1:
                return f_moves[0]
            elif len(r_moves) == 1:
                return r_moves[0]
            elif len(p_moves) == 1:
                return p_moves[0]
            elif len(moves) == 1:
                return moves[0]

        # If could not find a match listen again
        return self.play(board)
