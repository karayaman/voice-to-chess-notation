import pickle
from collections import defaultdict
from random import shuffle

pieces = {"N": ["knight", "night", "nike", "9", "nine", "ninth", "white", "flight", "light", "might"],
          "B": ["bishop", "ship"],
          "Q": ["queen", "quin", "green", "coin", "korean"],
          "K": ["king", "kink", "pink", "can", "sync", "qing", "ping", "change"],
          "": [""],
          "R": ["rook", "broke", "brook", "brooke", "ruk", "rooke", "rug", "rukh", "ruke", "route", "luke", "rup",
                "group", "rub", "crook", "rock", "rilke", "truck", "rue", "chuck", "ruck", "struck", "stroke", "rogue"]}
files = {"a": ["a", "aa", "eye", "hey", "i"], "b": ["b", "be", "bee", "by", "me", "p"], "c": ["c", "ce", "si", "sea"],
         "d": ["d", "de", "t", "ty", "the", "tea"],
         "e": ["e", "ee", "v", "yv", "y", "ye", "yee"],
         "f": ["f", "fe", "ff", "at"],
         "g": ["g", "ge", "j", "ja", "ji", "gi", "qi"], "h": ["h", "he", "age", "page", "paige"], "": [""]}
ranks = {"1": ["1", "one", "von", "van", "mon", "onne", "wang", "wong", "wan", "ven", "vaughn"],
         "2": ["2", "two", "to", "too", "ii"],
         "3": ["3", "three", "tree", "free"],
         "4": ["4", "four", "fore", "for", "fool", "full", "pool", "por", "poor", "force", "forth", "fault", "port",
               "fall"],
         "5": ["5", "five", "fight", "fife", "v"],
         "6": ["6", "six", "cigs", "sics", "stings", "sings", "tix"],
         "7": ["seven", "7"],
         "8": ["8", "eight"], "": [""]}

extra_data = [("95", "N5"), ("changeaah", "Ka8"), ("brookepaigega", "Rhg8"),
              ("epor", "e4"), ("ybor", "e4"), ("83", "a3"), ("84", "a4"), ("18", "a8"), ("indyto", "Qd2")]
extra_data = []  # Don't use extra data
data = []
for piece, piece_names in pieces.items():
    for piece_name in piece_names:
        for file, file_names in files.items():
            for file_name in file_names:
                for file2, file_names2 in files.items():
                    for file_name2 in file_names2:
                        if file == file2:
                            continue
                        for rank, rank_names in ranks.items():
                            for rank_name in rank_names:
                                name = piece_name + file_name + file_name2 + rank_name
                                notation = piece + file + file2 + rank
                                if file and file2:
                                    if piece not in ["", "N", "R"]:
                                        continue
                                    file_difference = abs(ord(file) - ord(file2))
                                    file_difference_allowed = 7
                                    if piece == "":
                                        file_difference_allowed = 1
                                    elif piece == "N":
                                        file_difference_allowed = 2
                                    if file_difference > file_difference_allowed:
                                        continue
                                data.append(
                                    (name, notation))

for piece, piece_names in pieces.items():
    for piece_name in piece_names:
        data.append((piece_name, piece))

for file, file_names in files.items():
    for file_name in file_names:
        data.append((file_name, file))

for rank, rank_names in ranks.items():
    for rank_name in rank_names:
        data.append((rank_name, rank))

# Always take longest notation if there are duplicate names
# longest = defaultdict(list)
# for name, notation in data:
#    longest[name].append(notation)

# for name in longest.keys():
#    longest[name].sort(key=lambda x: len(x), reverse=True)


# data = [(name, notations[0]) for name, notations in longest.items()]

# Always take shortest notation if there are duplicate names
shortest = defaultdict(list)
for name, notation in data:
    shortest[name].append(notation)

for name in shortest.keys():
    shortest[name].sort(key=lambda x: len(x))

data = [(name, notations[0]) for name, notations in shortest.items()]

data = list(set(data))

length_dict = defaultdict(int)
length_data = defaultdict(list)
for name, notation in data:
    length_dict[len(notation)] += 1
    length_data[len(notation)].append((name, notation))
shuffle(length_data[4])
length_data[4] = length_data[4][:len(length_data[3]) // 2]
data = length_data[1] + length_data[2] + length_data[3] + length_data[4] + extra_data
print(data)
print(len(data))
print(length_dict)
filename = 'data.bin'
outfile = open(filename, 'wb')
pickle.dump(data, outfile)
outfile.close()
