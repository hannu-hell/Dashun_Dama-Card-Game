from game import *
import os
import socket
import pickle
import threading


# Sets the position of the window to the coordinates
os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,50'

# Game
game = Game()
player1 = None
opponentPlayedCards = []
playerPlayedCards = []
gameOver = False
player2_start_game = False
gamesPlayed = 0
player2wins = 0


def reset_game():
    global game, player1, hand, player2_start_game
    del hand
    del game
    game = Game()
    player1 = None
    player2_start_game = False
    playerPlayedCards.clear()
    opponentPlayedCards.clear()


def game_logic(p1, p2):
    global gameOver, game, player2_start_game, gamesPlayed, player2wins
    playerPlayedCards.append(p2.playedCard)
    if player2_start_game is False:
        if p2.remainingCards != 0:
            if p1.playedCard.suit == p2.playedCard.suit:
                high_card = game.compare_cards(p1.playedCard, p2.playedCard)
                if high_card == p2.playedCard:
                    for i in playerPlayedCards:
                        p2.hand.insert(0, i)
                    for j in opponentPlayedCards:
                        p2.hand.insert(0, j)
                    p2.remainingCards = len(p2.hand)
                    print("-------PLAYER 2 has absorbed the cards-------")
                    print(f'You: {p2.playedCard}, Opponent: {p1.playedCard}')
                playerPlayedCards.clear()
                opponentPlayedCards.clear()
        else:
            p2.won = True
            gameOver = True



# Connections
HOST = ""
PORT = 9999
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST, PORT))
print("Connected to opponent")
hand = pickle.loads(c.recv(4096))
player2 = Player(hand)
player2.turn = False


# Creating Thread

def create_thread(target):
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()


def receiving_data():
    global player2, player1, gameOver, hand, player2_start_game, gamesPlayed, player2wins
    while True:
        data = pickle.loads(c.recv(4096))
        if type(data) == list:
            gamesPlayed += 1
            reset_game()
            hand = data
            if player2.won:
                player2wins += 1
                del player2
                player2 = Player(hand)
                player2.turn = False
            else:
                del player2
                player2 = Player(hand)
                player2_start_game = True
                player2.turn = True
            gameOver = False
        else:
            player1 = data
            if not player1.won:
                opponentPlayedCards.append(player1.playedCard)
                if player2_start_game:
                    if player1.remainingCards != 0:
                        if player2.remainingCards > 0:
                            if player1.playedCard.suit == player2.playedCard.suit:
                                high_card = game.compare_cards(player1.playedCard, player2.playedCard)
                                if high_card == player2.playedCard:
                                    for i in playerPlayedCards:
                                        player2.hand.insert(0, i)
                                    for j in opponentPlayedCards:
                                        player2.hand.insert(0, j)
                                    player2.remainingCards = len(player2.hand)
                                    print("-------PLAYER 2 has absorbed the cards-------")
                                    print(f'You: {player2.playedCard}, Opponent: {player1.playedCard}')
                                playerPlayedCards.clear()
                                opponentPlayedCards.clear()
                        else:
                            player2.won = True
                            gameOver = True
                    else:
                        gameOver = True
                player2.turn = True
            else:
                gameOver = True


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
o_card_num_rect = (220, 122, 30, 20)
p_card_num_rect = (220, 262, 30, 20)
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
    if player2.remainingCards != 0:
        surf.blit(card_back, ((winWidth//2-cardWidth//2), (winHeight-cardHeight-50)))
    if (player1 is None) or (player1.remainingCards != 0):
        surf.blit(card_back, ((winWidth//2-cardWidth//2), 50))
    back_fill(p_set_rect)
    back_fill(o_set_rect)
    display_cards_in_hands(surf, player2, player1)


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
    p_cards = str(player2.remainingCards)
    p_r_cards = font.render(p_cards, 1, (255, 255, 255))
    back_fill(p_card_num_rect)
    surf.blit(p_r_cards, (230, 265))
    if player1 is not None:
        o_cards = str(player1.remainingCards)
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
    surf.blit(you, (230, winHeight - 35))
    back_fill(o_rect)
    surf.blit(opponent, (230, 25))
    back_fill(cards_on_table_rect)
    c_on_table = font.render("Cards on Table: " + f'{len(playerPlayedCards) + len(opponentPlayedCards)}', 1, (255, 255, 0))
    surf.blit(c_on_table, (((winWidth/2) + 62), ((winHeight/2) - 13)))
    back_fill(p_games_rect)
    p_games = font.render("Games Played: " + f'{gamesPlayed}', 1, (255, 255, 0))
    surf.blit(p_games, (((winWidth/2) + 62), ((winHeight/2) + 22)))
    back_fill(p_win_rect)
    p_wins = font.render("WINS : " + f'{player2wins}', 1, (255, 128, 0))
    surf.blit(p_wins, (((winWidth / 2) + 62), (winHeight - cardHeight - 22)))
    back_fill(o_win_rect)
    o_wins = font.render("WINS : " + f'{gamesPlayed - player2wins}', 1, (255, 128, 0))
    surf.blit(o_wins, (((winWidth / 2) + 62), 82))


def draw_player_turn(surf):
    if not gameOver:
        if player2.turn:
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
    cont1 = font_cont.render("Wait for opponent", 1, (0, 255, 0))
    cont2 = font_cont.render("to play again", 1, (0, 255, 0))
    surf.blit(won, (((winWidth / 2) - 45), ((winHeight / 2)-10)))
    surf.blit(cont1, (((winWidth / 2) - 45), ((winHeight / 2)+20)))
    surf.blit(cont2, (((winWidth / 2) - 35), ((winHeight / 2)+35)))


def you_lost(surf):
    font = pygame.font.Font(None, 24)
    font_cont = pygame.font.Font(None, 15)
    pygame.draw.rect(surf, (0, 0, 0), playArea)
    lost = font.render("YOU LOST !", 1, (255, 128, 0))
    cont1 = font_cont.render("Wait for opponent", 1, (0, 255, 0))
    cont2 = font_cont.render("to play again", 1, (0, 255, 0))
    surf.blit(lost, (((winWidth / 2) - 45), ((winHeight / 2)-10)))
    surf.blit(cont1, (((winWidth / 2) - 45), ((winHeight / 2)+20)))
    surf.blit(cont2, (((winWidth / 2) - 35), ((winHeight / 2)+35)))


def play_area_update(surf):
    pygame.draw.rect(surf, (164, 90, 82), playArea)
    if not gameOver:
        if player2_start_game is False:
            if len(playerPlayedCards) != 0 and not player2.turn:
                match_cards(surf, playerPlayedCards[-1], placeCardRight[0], placeCardRight[1])
            if len(opponentPlayedCards) != 0:
                match_cards(surf, opponentPlayedCards[-1], placeCardLeft[0], placeCardLeft[1])
        else:
            if len(playerPlayedCards) != 0:
                match_cards(surf, playerPlayedCards[-1], placeCardRight[0], placeCardRight[1])
            if len(opponentPlayedCards) != 0 and player2.turn:
                match_cards(surf, opponentPlayedCards[-1], placeCardLeft[0], placeCardLeft[1])
    else:
        if player2.won:
            you_won(surf)
        else:
            you_lost(surf)


def window_update():
    draw_layout(win)
    draw_player_turn(win)
    play_area_update(win)
    draw_stats(win)
    pygame.display.update()


create_thread(receiving_data)


run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            c.close()
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and player2.turn and not gameOver:
            if pygame.mouse.get_pressed()[0]:
                if (winWidth//2 - cardWidth//2) <= pygame.mouse.get_pos()[0] <= (winWidth//2 + cardWidth//2):
                    if (winHeight-cardHeight-50) <= pygame.mouse.get_pos()[1] <= (winHeight-50):
                        player2.playedCard = player2.hand.pop()
                        player2.remainingCards -= 1
                        c.send(pickle.dumps(player2))
                        game_logic(player1, player2)
                        player2.turn = False
    window_update()


