from game import *
import os
import socket
import pickle
import threading
import random


# Sets the position of the window to the coordinates
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,50'


# Game
hand1 = None
hand2 = None
game = None
newGame = False
player2_start_game = False
gamesPlayed = 0
player1wins = 0


def initialize_game():
    global hand1, hand2, game
    game = Game()
    game.shuffle_deck()
    hand1 = game.deal_hand1()
    hand2 = game.deal_hand2()


def reset_game():
    global game, player1, player2, hand1, hand2, player2_start_game, gamesPlayed, player1wins
    del hand1
    del hand2
    del game
    gamesPlayed += 1
    player2 = None
    initialize_game()
    if player1.won:
        player1wins += 1
        del player1
        player1 = Player(hand1)
        player2_start_game = True
        player1.turn = False
    else:
        del player1
        player1 = Player(hand1)
        player2_start_game = False
        player1.turn = True
    playerPlayedCards.clear()
    opponentPlayedCards.clear()


initialize_game()
opponentPlayedCards = []
playerPlayedCards = []
gameOver = False
player1 = Player(hand1)
player2 = None
player1.turn = True


def game_logic(p1, p2):
    global gameOver, game, gamesPlayed, player1wins
    opponentPlayedCards.append(p2.playedCard)
    if player2_start_game is False:
        if p2.remainingCards != 0:
            if p1.remainingCards > 0:
                if p1.playedCard.suit == p2.playedCard.suit:
                    high_card = game.compare_cards(p1.playedCard, p2.playedCard)
                    if high_card == p1.playedCard:
                        for i in playerPlayedCards:
                            p1.hand.insert(0, i)
                        for j in opponentPlayedCards:
                            p1.hand.insert(0, j)
                        p1.remainingCards = len(p1.hand)
                        print("-------PLAYER 1 has absorbed the cards-------")
                        print(f'You: {player1.playedCard}, Opponent: {player2.playedCard}')
                    playerPlayedCards.clear()
                    opponentPlayedCards.clear()
            else:
                p1.won = True
                gameOver = True
                conn.send(pickle.dumps(p1))
        else:
            gameOver = True


# Connections
HOST = ""
PORT = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("Please wait for opponent to join")
conn = None
connection_established = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("Waiting for opponent to join")


# Creating Thread
def create_thread(target):
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()


def receive_data():
    global player2
    player2 = pickle.loads(conn.recv(4096))
    game_logic(player1, player2)
    player1.turn = True


def establish_connection():
    global conn, connection_established
    conn, address = s.accept()
    print("Connected to your opponent")
    connection_established = True
    conn.send(pickle.dumps(hand2))
    while True:
        receive_data()


# Graphics
pygame.init()

winWidth = 400
winHeight = 400
cardWidth = 47
cardHeight = 62
playArea = (((winWidth/2)-50), ((winHeight/2)-50), 100, 100)
placeCardLeft = (playArea[0]+2, playArea[1]+50-cardHeight//2)
placeCardRight = (playArea[0]+playArea[3]-2-cardWidth, playArea[1]+50-cardHeight//2)

win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("DASHUN_DAMA")

p_last_card = ((winWidth//2-cardWidth//2)-2, (winHeight-cardHeight-50)-2, 50, 65)
o_last_card = ((winWidth//2-cardWidth//2)-2, 48, 50, 65)
o_card_rect = (165, 122, 90, 20)
p_card_rect = (165, 262, 90, 20)
o_card_num_rect = (230, 122, 30, 20)
p_card_num_rect = (230, 262, 30, 20)
p_rect = (220, winHeight-38, 50, 20)
o_rect = (220, 22, 100, 20)
o_set_rect = (20, 20, 120, 170)
p_set_rect = (20, 210, 120, 170)
color = (0, 0, 0)
cards_on_table_rect = (((winWidth/2)+60), ((winHeight/2)-15), 125, 30)
p_games_rect = (((winWidth/2)+60), ((winHeight/2)+20), 125, 30)
p_win_rect = (((winWidth/2)+60), (winHeight-cardHeight-20), 80, 30)
o_win_rect = (((winWidth/2)+60), 80, 80, 30)


def back_fill(rectangle):
    pygame.draw.rect(win, color, rectangle)


def draw_layout(surf):
    pygame.draw.rect(surf, (255, 0, 0), (10, 10, 380, 380), 2)
    pygame.draw.rect(surf, (164, 90, 82), playArea)
    back_fill(p_last_card)
    back_fill(o_last_card)
    if player1.remainingCards != 0:
        surf.blit(card_back, ((winWidth//2-cardWidth//2), (winHeight-cardHeight-50)))
    if (player2 is None) or (player2.remainingCards != 0):
        surf.blit(card_back, ((winWidth//2-cardWidth//2), 50))
    back_fill(p_set_rect)
    back_fill(o_set_rect)
    display_cards_in_hands(surf, player1, player2)


def display_cards_in_hands(surf, p1, p2):
    p1_x_spacing, p2_x_spacing = 0, 0
    p1_y, p2_y = 300, 40
    if 0 < p1.remainingCards <= 10:
        for _ in range(p1.remainingCards-1):
            surf.blit(card_back, (25+p1_x_spacing, p1_y))
            p1_x_spacing += 5
    elif 10 < p1.remainingCards <= 20:
        for _ in range(10):
            surf.blit(card_back, (25+p1_x_spacing, p1_y))
            p1_x_spacing += 5
        p1_x_spacing = 0
        for _ in range(p1.remainingCards-10-1):
            surf.blit(card_back, (25+p1_x_spacing, p1_y-10))
            p1_x_spacing += 5
    elif 20 < p1.remainingCards <= 30:
        for _ in range(2):
            for _ in range(10):
                surf.blit(card_back, (25+p1_x_spacing, p1_y))
                p1_x_spacing += 5
            p1_x_spacing = 0
            p1_y -= 10
        for _ in range(p1.remainingCards-20-1):
            surf.blit(card_back, (25+p1_x_spacing, p1_y-10))
            p1_x_spacing += 5
    elif 30 < p1.remainingCards <= 40:
        for _ in range(3):
            for _ in range(10):
                surf.blit(card_back, (25+p1_x_spacing, p1_y))
                p1_x_spacing += 5
            p1_x_spacing = 0
            p1_y -= 10
        for _ in range(p1.remainingCards-30-1):
            surf.blit(card_back, (25 + p1_x_spacing, p1_y-10))
            p1_x_spacing += 5
    elif 40 < p1.remainingCards <= 52:
        for _ in range(4):
            for _ in range(10):
                surf.blit(card_back, (25 + p1_x_spacing, p1_y))
                p1_x_spacing += 5
            p1_x_spacing = 0
            p1_y -= 10
        for _ in range(p1.remainingCards-40-1):
            surf.blit(card_back, (25+p1_x_spacing, p1_y-10))
            p1_x_spacing += 5
    if p2 is not None:
        if 0 < p2.remainingCards <= 10:
            for _ in range(p2.remainingCards - 1):
                surf.blit(card_back, (25 + p2_x_spacing, p2_y))
                p2_x_spacing += 5
        elif 10 < p2.remainingCards <= 20:
            for _ in range(10):
                surf.blit(card_back, (25 + p2_x_spacing, p2_y))
                p2_x_spacing += 5
            p2_x_spacing = 0
            for _ in range(p2.remainingCards - 10 - 1):
                surf.blit(card_back, (25 + p2_x_spacing, p2_y+10))
                p2_x_spacing += 5
        elif 20 < p2.remainingCards <= 30:
            for _ in range(2):
                for _ in range(10):
                    surf.blit(card_back, (25 + p2_x_spacing, p2_y))
                    p2_x_spacing += 5
                p2_x_spacing = 0
                p2_y += 10
            for _ in range(p2.remainingCards - 20 - 1):
                surf.blit(card_back, (25 + p2_x_spacing, p2_y+10))
                p2_x_spacing += 5
        elif 30 < p2.remainingCards <= 40:
            for _ in range(3):
                for _ in range(10):
                    surf.blit(card_back, (25 + p2_x_spacing, p2_y))
                    p2_x_spacing += 5
                p2_x_spacing = 0
                p2_y += 10
            for _ in range(p2.remainingCards - 30 - 1):
                surf.blit(card_back, (25 + p2_x_spacing, p2_y+10))
                p2_x_spacing += 5
        elif 40 < p2.remainingCards <= 52:
            for _ in range(4):
                for _ in range(10):
                    surf.blit(card_back, (25 + p2_x_spacing, p2_y))
                    p2_x_spacing += 5
                p2_x_spacing = 0
                p2_y += 10
            for _ in range(p2.remainingCards - 40 - 1):
                surf.blit(card_back, (25 + p2_x_spacing, p2_y+10))
                p2_x_spacing += 5
    else:
        for _ in range(2):
            for _ in range(10):
                surf.blit(card_back, (25 + p2_x_spacing, p2_y))
                p2_x_spacing += 5
            p2_x_spacing = 0
            p2_y += 10
        for _ in range(5):
            surf.blit(card_back, (25 + p2_x_spacing, p2_y + 10))
            p2_x_spacing += 5


def draw_stats(surf):
    font = pygame.font.Font(None, 20)
    cards = font.render("CARDS: ", 1, (0, 128, 255))
    back_fill(o_card_rect)
    surf.blit(cards, (170, 125))
    back_fill(p_card_rect)
    surf.blit(cards, (170, 265))
    p_cards = str(player1.remainingCards)
    p_r_cards = font.render(p_cards, 1, (255, 255, 255))
    back_fill(p_card_num_rect)
    surf.blit(p_r_cards, (230, 265))
    if player2 is not None:
        o_cards = str(player2.remainingCards)
        o_r_cards = font.render(o_cards, 1, (255, 255, 255))
        back_fill(o_card_num_rect)
        surf.blit(o_r_cards, (230, 125))
    else:
        o_r_cards = font.render("26", 1, (255, 255, 255))
        back_fill(o_card_num_rect)
        surf.blit(o_r_cards, (230, 125))
    you = font.render("YOU", 1, (255, 255, 255))
    opponent = font.render("OPPONENT", 1, (255, 255, 255))
    back_fill(p_rect)
    surf.blit(you, (230, winHeight-35))
    back_fill(o_rect)
    surf.blit(opponent, (230, 25))
    back_fill(cards_on_table_rect)
    c_on_table = font.render("Cards on Table: " + f'{len(playerPlayedCards)+len(opponentPlayedCards)}', 1, (255, 255, 0))
    surf.blit(c_on_table, (((winWidth/2)+62), ((winHeight/2)-13)))
    back_fill(p_games_rect)
    p_games = font.render("Games Played: " + f'{gamesPlayed}', 1, (255, 255, 0))
    surf.blit(p_games, (((winWidth/2)+62), ((winHeight/2)+22)))
    back_fill(p_win_rect)
    p_wins = font.render("WINS : " + f'{player1wins}', 1, (255, 128, 0))
    surf.blit(p_wins, (((winWidth/2)+62), (winHeight-cardHeight-22)))
    back_fill(o_win_rect)
    o_wins = font.render("WINS : " + f'{gamesPlayed-player1wins}', 1, (255, 128, 0))
    surf.blit(o_wins, (((winWidth/2)+62), 82))


def draw_player_turn(surf):
    if not gameOver:
        if player1.turn:
            pygame.draw.circle(surf, (255, 0, 0), (winWidth // 2, 30), 10)
            pygame.draw.circle(surf, (0, 255, 0), (winWidth // 2, 370), 10)
        else:
            pygame.draw.circle(surf, (0, 255, 0), (winWidth // 2, 30), 10)
            pygame.draw.circle(surf, (255, 0, 0), (winWidth // 2, 370), 10)
    else:
        pygame.draw.circle(surf, (255, 0, 0), (winWidth // 2, 30), 10)
        pygame.draw.circle(surf, (255, 0, 0), (winWidth // 2, 370), 10)


def you_won(surf):
    font = pygame.font.Font(None, 24)
    font_cont = pygame.font.Font(None, 15)
    pygame.draw.rect(surf, (0, 0, 0), playArea)
    won = font.render("YOU WON !", 1, (255, 128, 0))
    cont1 = font_cont.render("Press Space", 1, (0, 255, 0))
    cont2 = font_cont.render("to play again", 1, (0, 255, 0))
    surf.blit(won, (((winWidth / 2) - 45), ((winHeight / 2)-10)))
    surf.blit(cont1, (((winWidth / 2) - 35), ((winHeight / 2)+20)))
    surf.blit(cont2, (((winWidth / 2) - 35), ((winHeight / 2)+35)))


def you_lost(surf):
    font = pygame.font.Font(None, 24)
    font_cont = pygame.font.Font(None, 15)
    pygame.draw.rect(surf, (0, 0, 0), playArea)
    lost = font.render("YOU LOST !", 1, (255, 128, 0))
    cont1 = font_cont.render("Press Space", 1, (0, 255, 0))
    cont2 = font_cont.render("to play again", 1, (0, 255, 0))
    surf.blit(lost, (((winWidth / 2) - 45), ((winHeight / 2)-10)))
    surf.blit(cont1, (((winWidth / 2) - 35), ((winHeight / 2)+20)))
    surf.blit(cont2, (((winWidth / 2) - 35), ((winHeight / 2)+35)))


def play_area_update(surf):
    pygame.draw.rect(surf, (164, 90, 82), playArea)
    if not gameOver:
        if player2_start_game is False:
            if len(playerPlayedCards) != 0:
                match_cards(surf, playerPlayedCards[-1], placeCardLeft[0], placeCardLeft[1])
            if len(opponentPlayedCards) != 0 and player1.turn:
                match_cards(surf, opponentPlayedCards[-1], placeCardRight[0], placeCardRight[1])
        else:
            if len(playerPlayedCards) != 0 and not player1.turn:
                match_cards(surf, playerPlayedCards[-1], placeCardLeft[0], placeCardLeft[1])
            if len(opponentPlayedCards) != 0:
                match_cards(surf, opponentPlayedCards[-1], placeCardRight[0], placeCardRight[1])
    else:
        if player1.won:
            you_won(surf)
        else:
            you_lost(surf)


def window_update():
    draw_layout(win)
    draw_player_turn(win)
    play_area_update(win)
    draw_stats(win)
    pygame.display.update()


create_thread(establish_connection)


run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s.close()
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and player1.turn and not gameOver and connection_established:
            if pygame.mouse.get_pressed()[0]:
                if (winWidth//2 - cardWidth//2) <= pygame.mouse.get_pos()[0] <= (winWidth//2 + cardWidth//2):
                    if (winHeight-cardHeight-50) <= pygame.mouse.get_pos()[1] <= (winHeight-50):
                        player1.playedCard = player1.hand.pop()
                        player1.remainingCards -= 1
                        conn.send(pickle.dumps(player1))
                        playerPlayedCards.append(player1.playedCard)
                        if player2_start_game:
                            if player2.remainingCards != 0:
                                if player1.remainingCards > 0:
                                    if player1.playedCard.suit == player2.playedCard.suit:
                                        high_card = game.compare_cards(player1.playedCard, player2.playedCard)
                                        if high_card == player1.playedCard:
                                            for i in playerPlayedCards:
                                                player1.hand.insert(0, i)
                                            for j in opponentPlayedCards:
                                                player1.hand.insert(0, j)
                                            player1.remainingCards = len(player1.hand)
                                            print("-------PLAYER 1 has absorbed the cards-------")
                                            print(f'You: {player1.playedCard}, Opponent: {player2.playedCard}')
                                        playerPlayedCards.clear()
                                        opponentPlayedCards.clear()
                                else:
                                    player1.won = True
                                    gameOver = True
                                    conn.send(pickle.dumps(player1))
                            else:
                                gameOver = True
                        player1.turn = False
        if event.type == pygame.KEYDOWN and gameOver:
            if event.key == pygame.K_SPACE:
                reset_game()
                conn.send(pickle.dumps(hand2))
                gameOver = False
    window_update()


