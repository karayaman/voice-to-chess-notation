import pickle
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, TimeDistributed, RepeatVector, Dense
from keras.callbacks import EarlyStopping

from random import shuffle

filename = 'data.bin'
infile = open(filename, 'rb')
data = pickle.load(infile)
infile.close()

print(data)


def prepare(data):
    shuffle(data)
    data_x, data_y = [], []
    encode_next_value = 1
    encode_dict = {}
    for x, y in data:
        data_x.append(x)
        data_y.append(y)
        for c in x:
            if c not in encode_dict:
                encode_dict[c] = encode_next_value
                encode_next_value += 1
        for c in y:
            if c not in encode_dict:
                encode_dict[c] = encode_next_value
                encode_next_value += 1
    return data_x, data_y, encode_dict, encode_next_value


def one_hot_encode(rows, max_len):
    encoding = np.zeros((len(rows), max_len, encode_next_value), dtype=np.bool)
    for i, s in enumerate(rows):
        for j, c in enumerate(s):
            v = encode_dict[c]
            encoding[i][j][v] = 1
        for j in range(len(s), max_len):  # padding
            v = 0
            encoding[i][j][v] = 1
    return encoding


data_x, data_y, encode_dict, encode_next_value = prepare(data)
max_len_x = max(len(x) for x in data_x)
max_len_y = max(len(y) for y in data_y)

decode_dict = {value: key for key, value in encode_dict.items()}
decode_dict[0] = "*"

x = one_hot_encode(data_x, max_len_x)
y = one_hot_encode(data_y, max_len_y)

hidden_size = 128
batch_size = 128

model = Sequential()
model.add(LSTM(hidden_size, input_shape=(max_len_x, encode_next_value)))
model.add(RepeatVector(max_len_y))
model.add(LSTM(hidden_size, return_sequences=True))
model.add(TimeDistributed(Dense(encode_next_value, activation='softmax')))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
history = model.fit(x, y,
                    epochs=300,
                    batch_size=batch_size,
                    validation_split=0.4,
                    callbacks=[es]
                    )

save_file = [decode_dict, encode_next_value, encode_dict, max_len_x]
filename = 'machinelearning.bin'
outfile = open(filename, 'wb')
pickle.dump(save_file, outfile)
outfile.close()

model.save("my_model")