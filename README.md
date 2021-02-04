# voice-to-chess-notation
Program that recognizes your speech and enables you to play chess using your voice.  To make a move, you should say the move you want to play in terms of chess notation. After that, program should recognize your speech and make the necessary clicks to make the move.



To properly use the program you should take screenshots of chess board at starting position, one for when you play white and one for when you play black and save them as "white.JPG" and "black.JPG" similar to the images included in the source code. After that you can run main.py to start the program. Before using the program in an actual game you should turn off all the animations to prevent any unwanted behavior.



You can start using the program either pressing "Start playing (s)" button from the GUI or pressing key "S". After that program will use computer vision to detect the chessboard you are playing. From now on you should not move your mouse or use your keyboard to prevent any unwanted behavior. You can now say the move you want to play in terms of chess notation and see that program actually makes the move on the chess board. If it does not make the move, you can say the move again after 5 seconds. Sometimes program won't be able to find the move you want to play and chooses not to make a move instead of making a random move. 

## Required libraries
- speech_recognition
- tensorflow
- keras
- opencv
- python-chess
- pyautogui
- mss
- numpy