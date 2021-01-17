import pickle

pieces = {"N": ["knight", "night", "nike", "9", "nine"], "B": ["bishop"], "Q": ["queen", "quin"], "K": ["king"],
          "": [""], "R": ["rook", "brook"]}
files = {"a": ["a", "aa"], "b": ["b", "be"], "c": ["c", "ce"], "d": ["d", "de"], "e": ["e", "ee", "v"],
         "f": ["f", "fe", "ff", "at", "s"],
         "g": ["g", "ge"], "h": ["h", "he", "age"], "": [""]}
ranks = {"1": ["1", "one"], "2": ["2", "two"], "3": ["3", "three", "tree"],
         "4": ["4", "four", "fore", "for"], "5": ["5", "five"], "6": ["6", "six", "cigs", "sics"], "7": ["seven", "7"],
         "8": ["8", "eight"]}

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
                                data.append(
                                    (piece_name + file_name + file_name2 + rank_name, piece + file + file2 + rank))

for piece, piece_names in pieces.items():
    for piece_name in piece_names:
        data.append((piece_name, piece))

for file, file_names in files.items():
    for file_name in file_names:
        data.append((file_name, file))

for rank, rank_names in ranks.items():
    for rank_name in rank_names:
        data.append((rank_name, rank))

print(data)
print(len(data))
filename = 'data.bin'
outfile = open(filename, 'wb')
pickle.dump(data, outfile)
outfile.close()
