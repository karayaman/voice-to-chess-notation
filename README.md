# voice-to-chess-notation
Program that recognizes your speech and enables you to type chess notation using your voice. This way you can play chess using your voice on the platforms which support keyboard input. To make a move, you should say the move you want to play in terms of chess notation. After that, program should recognize your speech and type the move. Then, if you say "play", program will simulate pressing enter so that the move can be played. If program typed the move incorrectly, you can say "cancel" and program will undo the typing. 

## Required libraries
- speech_recognition
- pynput
- keras