# DASHUN DAMA (DD) Card Game

Dashun Dama is a very simple card game played in the Maldives.  This game is a two player game and can be played online.  A pack of 52 cards are divided into two hands after a shuffle and flipped over so that the players arent allowed to see what cards they have in their hands.  Player 1 starts off the game by placing a card from the bottom of his/her hand and then Player 2 places a card from his/her hand.  If both the cards match in suits, the player who played the higher value card of that suit gets (absorbs) both the cards.  Otherwise if the suits don't match, the cards are kept on the table and the playing continues until a match is made.  Once a match has been made the player with the higher value card of that suit who played in that turn absorbs all the cards on the table. The player who absorbs the cards places the cards on top of his/her hand. The objective of the game is to empty one's own hand.  The player who empties his/her hand first wins the game.  Like I said its a fairly simple game, but has a certain element of suspense if cards keep stacking on the table without a match. 

## How the game is set:

Player 1 (server) starts off the very first game.  Once a game has ended and if player 1 wins, the next game will be started off by player 2 (client) and if player 2 has won a game, the next will be started by player 1 and its goen on like that.

Players can see how many cards they have in their hand which is updated visually as cards and as a figure.  The number of cards on the table at a time are also displayed as a figure.  Each player can play a card by clicking the card which is set in the bottom middle of the screen.  

If a player absorbs the cards, it will be printed on to the console with the card that was played by the player and the opponent. Players will be able to visually see the cards played if a match hasn't been made.

In order to run the game, each player would need to unpack the card_pack folder and place the card pngs and the other two files (if player 1 - server.py and game.py, if player 2 - client.py and game.py) in the same folder.

This game runs on python3 and the only external library used is the pygame library which can be downloaded using pip/pip3.  

- Credit for the png images of the card pack goes to: Andrew Tidey http://creativecommons.org/publicdomain/zero/1.0/

Licensed under [MIT License](LICENSE) 
Thanks

