import pickle
import numpy as np
from keras.models import load_model
from chess import square_name
import speech_recognition as sr
from collections import defaultdict


class Voice_to_chess_notation:
    def __init__(self, engine):
        filename = 'machinelearning.bin'
        infile = open(filename, 'rb')
        self.decode_dict, self.encode_next_value, self.encode_dict, self.max_len_x = pickle.load(infile)
        infile.close()
        self.model = load_model("my_model")
        self.r = sr.Recognizer()
        # with sr.Microphone() as source:
        #    self.r.adjust_for_ambient_noise(source)

        self.engine = engine

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
        return ''.join(self.decode_dict[c] for c in x if self.decode_dict[c] != '*')

    def convert_to_notation(self, response):
        notations = []
        for alternative in response["alternative"]:
            phrase = alternative["transcript"]
            phrase = phrase.lower()
            phrase = "".join(c for c in phrase if c.isalnum())
            if len(phrase) > self.max_len_x:
                phrase = phrase[:self.max_len_x]
            if phrase.isnumeric():
                continue
            print(phrase)
            phrase = self.one_hot_encode(phrase, self.max_len_x)
            preds = self.model.predict_classes(phrase, verbose=0)
            notation = self.one_hot_decode(preds[0])
            notations.append(notation)
        return notations

    def listen(self):
        phrase_time_limit = 5
        timeout = 10

        with sr.Microphone() as source:
            while True:
                try:
                    self.r.adjust_for_ambient_noise(source)
                    state = "SPEAK!"
                    print(state)
                    self.engine.say(state)
                    self.engine.runAndWait()
                    audio = self.r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                    self.engine.say("got it")
                    self.engine.runAndWait()
                    response = self.r.recognize_google(audio, language="en-GB", show_all=True)
                    print(response)
                    if not response:
                        continue
                    return self.convert_to_notation(response)
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
                    self.engine.say("Request Error!")
                    self.engine.runAndWait()
                except sr.UnknownValueError:
                    print("unknown error occured")
                    self.engine.say("unknown error occured")
                    self.engine.runAndWait()
                except sr.WaitTimeoutError:
                    print("Wait time out")
                    self.engine.say("Wait time out")
                    self.engine.runAndWait()

    def play(self, board):
        epsilon = 1.0
        decay_rate = 0.8
        threshold = 0.2
        move_candidates = defaultdict(float)
        notations = self.listen()
        print("Notations")
        print(notations)
        recycle = defaultdict(float)
        for notation in notations:
            start_piece, start_file, start_rank, end_file, end_rank = "P", "", "", "", ""
            piece_found, file_found, rank_found = 0, 0, 0
            for c in notation:
                if c.isupper():
                    start_piece = c
                    piece_found = 1
                elif c.islower():
                    if end_file:
                        start_file = end_file
                    end_file = c
                    file_found = 1
                elif c.isdigit():
                    if end_rank:
                        start_rank = end_rank
                    end_rank = c
                    rank_found = 1

            if file_found == 0 or rank_found == 0:
                print("Not enough information " + notation)
                recycle[notation] += epsilon
                continue

            moves = list(board.legal_moves)
            r_moves = [move for move in moves if square_name(move.to_square)[1] == end_rank or end_rank == ""]
            f_moves = [move for move in r_moves if square_name(move.to_square)[0] == end_file or end_file == ""]
            p_moves = [move for move in f_moves if board.piece_at(move.from_square).symbol().upper() == start_piece]
            sf_moves = [move for move in p_moves if square_name(move.from_square)[0] == start_file]
            sr_moves = [move for move in p_moves if square_name(move.from_square)[1] == start_rank]

            move_candidate = None

            score = epsilon

            if len(sr_moves) == 1 and start_file == "" and start_rank != "":
                move_candidate = sr_moves[0]
                # Check if it is necessary to specify start rank
                to_square_move_count = sum(move.to_square == move_candidate.to_square for move in p_moves)
                if to_square_move_count == 1:
                    move_candidate = None
                    print("Start rank is specified but it was not necessary")
                    recycle[notation] += epsilon
                else:
                    # It is difficult and rare to specify start rank so magnify the score
                    score *= len(notations)
            elif len(sf_moves) == 1 and start_file != "" and start_rank == "":
                move_candidate = sf_moves[0]
                # Check if it is necessary to specify start file
                to_square_move_count = sum(move.to_square == move_candidate.to_square for move in p_moves)
                if to_square_move_count == 1:
                    move_candidate = None
                    print("Start file is specified but it was not necessary")
                    recycle[notation] += epsilon
                else:
                    # It is difficult and rare to specify start file so magnify the score
                    score *= len(notations)
            elif len(p_moves) == 1 and start_file == "" and start_rank == "":
                move_candidate = p_moves[0]
            else:
                print("More than one move " + notation + str([sr_moves, sf_moves, p_moves, f_moves, r_moves, moves]))
                recycle[notation] += epsilon

            if move_candidate:
                for r_notation, r_epsilon in recycle.items():
                    if notation.startswith(r_notation):
                        score += r_epsilon
                move_candidates[move_candidate] += score

            epsilon *= decay_rate

        move_candidates = [(val, key) for key, val in move_candidates.items()]
        move_candidates.sort(reverse=True)
        print("Move candidates")
        print(move_candidates)
        if len(move_candidates) > 1 and abs(move_candidates[0][0] - move_candidates[1][0]) <= threshold:
            # If not sure listen again
            print("Could not decide a move")
            return self.play(board)
        elif move_candidates:
            if move_candidates[0][0] < (1.0 - threshold):
                print("Move candidate is not strong enough")
                return self.play(board)
            else:
                return move_candidates[0][1]
        else:
            # If could not find a match listen again
            print("No candidate moves")
            return self.play(board)
