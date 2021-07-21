# Checkers
Just a simple implementation of the [checkers/draughts](https://en.wikipedia.org/wiki/Draughts) game made in [PyGame](https://www.pygame.org/).
<br></br>
<img src="./imgs/checkers.PNG" alt="checkers" width="400"/>
## Installing
Python is required to run and play the game as of now. This was created using [Python 3.7.2](https://www.python.org/downloads/release/python-372/)
<br></br>
Additional Python packages need to be installed which can be seen in `requirements.txt` file.
<br></br>
All of these packages can be installed using:  
`pip install -r requirements.txt`
## Running
Simply call `python checkers.py` to run the program after all of the packages have been installed.
### Playing locally
### Playing online 
## TODO
- [ ] Finish host and client scripts to make the game playable online.
    - Allow host to specify port.
    - Allow client to specify IP and port.
- [ ] Finish making the menus.
    - Main menu
    - Game over menu
    - Host/connect menu
- [ ] Multiple modes
    - ~~Standard~~
    - Casual
    - International
- [ ] Reorganization (tidy `game.py`, etc.).
- [ ] Move limit so that game ends after a certain number of moves without capturing.
- [ ] Option to rotate the board when move is complete (not for online).
- [ ] Allow players to choose colors.
- [ ] Write comments. 
- [ ] Make program an executable.
