# Checkers

Just a simple implementation of the [checkers/draughts](https://en.wikipedia.org/wiki/Draughts) game made in [PyGame](https://www.pygame.org/). <br/>

<img src="./imgs/checkers.PNG" alt="checkers" width="400"/>

## Installing

Python is required to run and play the game as of now. This was created using [Python 3.7.2](https://www.python.org/downloads/release/python-372/) <br>

Only requirement as of now is **PyGame** which can be installed using the command <br/>

<u>**On Windows:**</u> <br/>

``` pip install pygame``` <br/>

<u>**On Unix/Mac:**</u>  

``` pip3 install pygame```

### Playing locally <br/>

To play locally, all you need to do is launch the game using the command 

<u>**On Windows:**</u>  

```python game.py```<br/>

<u>**On Unix/Mac:**</u>  

```python3 game.py```<br/>

### Playing online 

To play online, one player needs to host the game and the other player needs to connect to the game. <br/>

By default games will be hosted at **IP** *localhost (127.0.0.1)* and **port** *5000*.  

#### Hosting

<u>**On Windows:**</u>  

```python online.py host```<br/>

<u>**On Unix/Mac:**</u>  

```python3 online.py host```<br/>

#### Joining

<u>**On Windows:**</u>  

```python online.py cli```<br/>

<u>**On Unix/Mac:**</u>  

```python3 online.py cli```<br/>

#### Specifying the IP and port

When hosting or joining a game **`--ip IP`** and **`--port PORT`** can be used to specify the IP and port.

#### ```online.py``` as a whole

```
usage: online.py [-h] [--ip IP] [--port PORT] {host,cli}

Host or join a checkers game.

positional arguments:
  {host,cli}   determines whether to host or join a game

optional arguments:
  -h, --help   show this help message and exit
  --ip IP      IP address to host/connect
  --port PORT  port to host/connect
```

## TODO
- [ ] Add more gifs and images to README
- [ ] Finish host and client scripts to make the game playable online.
    - ~~Allow host to specify port.~~
    - ~~Allow client to specify IP and port.~~
    - Make GUI for online play.
- [ ] Reimplement resizing of the window
- [ ] Multiple modes
    - ~~Standard~~
    - Casual
    - International
- [ ] Reorganization
- [ ] Move limit so that game ends after a certain number of moves without capturing.
- [ ] Option to rotate the board when move is complete (not for online).
- [ ] Allow players to choose colors.
- [ ] Write comments. 
- [ ] Make program an executable.
