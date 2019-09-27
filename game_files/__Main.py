#!/usr/bin/python3

import time
import random
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.window import *


random.seed()


GAME_STATE = 0

fase = 0

difficulty = 1
GAME_SPEED = 1 * difficulty
# Largura da janela
width = 640

# Altura da janela
height = 480

# Cor de fundo
background_color = [0, 0, 20]

#Mostrar FPS
FPS = True

highscore = 0

# Titulo da janela
title = "Space Invaders"

window = Window(width, height)
window.set_title(title)
window.set_background_color(background_color)

keyboard = window.get_keyboard()
mouse = window.get_mouse()


# Sprite da nave do jogador
player = Sprite("Imagens/enemy/player.png")
vida = Sprite("Imagens/cora.png")
vida2 = Sprite("Imagens/coraf.png")
vidaVar = 3

# Posição inicial
player.set_position((window.width - player.width) / 2, (window.height - player.height))

# Velocidade do jogador
player.speed = 200

# Direção do jogador
player.direction = -1  # [cima]

# Pontuação
player.score = 0

background_01 = GameImage("Imagens/star.png")
background_02 = GameImage("Imagens/star.png")
# Sprite dos inimigos
enemy_image = "Imagens/enemy/minion"

boom = Sprite("Imagens/enemy/boom.png", 12)
boom.set_total_duration(250)
boom.set_loop(False)
boom.hide()


background_01.y = 0
background_02.y = -background_02.height

# Velocidade de rolagem
background_roll_speed = 50
# Velocidade dos inimigos
enemy_speed = 100

# Direção dos inimigos
enemy_direction = 1  # [baixo]



bullets = []

enemies = [[0 for x in range(4)] for x in range(8)]

enemy_shoot_delay = 1 / GAME_SPEED
player.shoot_delay = 1 / GAME_SPEED * 0.5

player.shoot_tick = player.shoot_delay


def win():
    """
    Função para verificar se o jogador ganhou
    Caso afirmativo, reinicia o jogo
    """

    # Criamos o acesso às variáveis globais
    global matrix_x
    global matrix_y
    global GAME_STATE
    global fase

    # Criamos uma variável de controle, para sabermos se o jogador ganhou o jogo
    won = True

    # Verifica em todas as linhas se ainda existe algum inimigo vivo
    for row in range(matrix_x):
        if won:
            for column in range(matrix_y):
                if enemies[row][column] != 0:
                    # Se ele encontrar algum inimigo vivo, seta a variável
                    # won como False e quebra a cadeia de repetições
                    won = False
                    break

    if won:
        # Se o jogo percorrer toda a matriz e não encontrar
        # nenhum inimigo vivo, reinicia o jogo
        GAME_STATE = 1
        if fase < 3:
            fase+=1
            difficulty = fase
            restart(player, enemies, bullets)
        elif fase == 3:
            GAME_STATE == 0
            fase = 0
            restart_window()



def spawn_enemy(i, j, enemy_matrix):
    """
    Gera a matriz de inimigos
    :param i: numero de linhas na matriz
    :param j: numero de colunas na matriz
    :param enemy_matrix: matriz de inimigos
    """

    # for x e for y percorrem cada elemento da matriz
    for x in range(i):
        for y in range(j):

            enemy = Sprite(enemy_image + str(random.randint(1, 3)) + ".png", 2)
            enemy.set_total_duration(1000)

            enemy.set_position(x * 80, y * 50)

            enemy.direction = 1

            enemy.shoot_delay = random.uniform(0, 10) / (GAME_SPEED * difficulty) 

            enemy.shoot_tick = 0

            enemy_matrix[x][y] = enemy



def restart(player, enemies, bullets):
    """
    Função para (re)iniciar o jogo.
    :param player: jogador
    :param enemies: matriz de inimigos
    :param bullets: lista de instancias de balas
    """

    # Gera o acesso às variáveis globais
    global matrix_x
    global matrix_y

    # Deleta todos os objetos enemies e bullets
    #del enemies
    for b in bullets:
    	del b
    

    # Retorna o jogador à posição e pontuação inicial do jogo
    if fase ==0:
    	player.score = 0
    	vidaVar=3



    player.set_position((window.width - player.width) / 2,(window.height - player.height))

    # Reinicia os contadores de disparos
    player.shoot_tick = player.shoot_delay

    # Cria uma nova matriz de inimigos
    matrix_x = int(random.uniform(3+difficulty, 8))
    matrix_y = int(random.uniform(1+difficulty, 4))
    spawn_enemy(matrix_x, matrix_y, enemies)


def adjust_bullet(actor, bullet):
    """
    Recebe o atirador e a bala, e ajusta sua posição
    :param actor: Instancia do jogador ou inimigo
    :param bullet: Instancia do projétil
    """

    # Calcula posição X da bala, utilizando como referência o
    # centro do ator e armazena em x_fire
    x_fire = actor.x + (actor.width / 2) - (bullet.width / 2)

    # Calcula posição Y do projétil, utilizando como referência
    # a direção de movimento e o tamanho do jogador, salvando
    # o resultado na variável y_fire
    if actor.direction == -1:
        y_fire = actor.y
    elif actor.direction == 1:
        y_fire = actor.y + actor.height - bullet.height

    # Transfere o valor das variáveis auxiliares x_fire e y_fire
    # para o projétil
    bullet.x = x_fire
    bullet.y = y_fire

    # Define direção do projétil
    bullet.direction = actor.direction


def shoot(shooter):
    """
    Cria um bullet, associando-o a um ator
    :param shooter: Ator responsável pelo disparo (jogador ou inimigo)
    """



    # Zera o contador de último disparo
    shooter.shoot_tick = 0

    # Cria uma nova bullet, dependendo de quem for que atirou
    if shooter.direction == -1:
        b = Sprite("Imagens/enemy/bullet.png", 2)
        b.set_total_duration(100)
    elif shooter.direction == 1:
        b = Sprite("Imagens/enemy/enemy_bullet.png", 5)
        b.set_total_duration(100)

    # Ajusta a posição inicial e a direção do projétil
    adjust_bullet(shooter, b)

    # Adiciona o novo projétil que criamos para ser desenhado na tela
    bullets.append(b)


def update_counters():
    """
    Atualiza contadores do jogo
    """

    # Atualiza o contador de controle de tiro do jogador
    player.shoot_tick += window.delta_time()

    # Atualiza o contador de controle de tiro de cada inimigo
    # presente na matriz de inimigos
    for row in range(matrix_x):
        for column in range(matrix_y):
            if enemies[row][column] != 0:
                enemies[row][column].shoot_tick += window.delta_time()


def scrolling(bg_bottom, bg_top, roll_speed):
    """
    Recebe dois background e a velocidade que devem rolar infinitamente
    :param bg_bottom: Sprite do fundo 1
    :param bg_top: Sprite do fundo 2
    :param roll_speed: Velocidade de deslocamento dos fundos
    """

    # Movimenta ambos os Sprites verticalmente
    bg_bottom.y += roll_speed * window.delta_time()
    bg_top.y += roll_speed * window.delta_time()

    # Se a imagem do topo já tiver sido completamente exibida,
    # retorna ambas imagens às suas posições iniciais
    if bg_top.y >= 0:
        bg_bottom.y = 0
        bg_top.y = -bg_top.height

    # Renderiza as duas imagens de fundo
    bg_bottom.draw()
    bg_top.draw()
def player_shoot():
    """
    Ação de atirar
    """
    # Verifica se o jogador apertou o botão de disparar
    if keyboard.key_pressed("SPACE"):
        # Verifica se já pode disparar
        if player.shoot_tick > player.shoot_delay:
            # Chama a função shoot(), para que ela efetue do disparo
            shoot(player)


def player_movement():
    """
    Ação de movimento da nave do jogador
    """

    # Atualiza a posição do jogador
    player.move_key_x(player.speed * window.delta_time() * GAME_SPEED)

    # Não permite que a lateral esquerda da nave ultrapasse a
    # lateral esquerda da tela, onde x = 0
    if player.x <= 0:         player.x = 0  # Não permite que a lateral esquerda da nave ultrapasse a
    #  lateral direita da tela, onde x = largura da tela.
    if player.x + player.width >= window.width:
        player.x = window.width - player.width


def bullet_movement():
    """
    Realiza a movimentação de cada bala em jogo
    """

    # Para cada bala instanciada no jogo
    for b in bullets:

        # Atualiza a sua posição, baseado em sua direção
        b.move_y(200 * b.direction * window.delta_time() * GAME_SPEED * difficulty)

        # Verifica se saiu da tela e, caso tenha saído, destrói o projétil
        if b.y < -b.height or b.y > window.height + b.height:
            bullets.remove(b)


def enemy_movement():
    """
    Realiza a movimentação de cada inimigo
    """

    # Acessando variáveis globais
    global enemy_direction
    global enemy_speed

    # Cria variável de controle
    inverted = False

    # Calcula a nova posição da matriz de inimigos
    new_position = enemy_speed * enemy_direction * window.delta_time() * GAME_SPEED

    # Percorre toda a matriz de inimigos
    for row in range(matrix_x):
        for column in range(matrix_y):
            # Caso a posição esteja preenchida, isto é, o inimigo
            # ainda esteja vivo, efetua as ações em seguida
            if enemies [row][column] != 0:
                # Move o inimigo para sua nova posição
                enemies[row][column].move_x(new_position)
                # Caso já tenha alcançado o intervalo de disparo,
                # efetua um novo disparo

                if enemies[row][column].shoot_tick > enemies[row][column].shoot_delay:

                    shoot(enemies[row][column])
                    enemies[row][column].shoot_tick = 0
                    enemies[row][column].shoot_delay = random.uniform(0, 15) / GAME_SPEED

                if not inverted:
                    # Se bateu na parede, então inverte a direção da matriz
                    # Altera direção para direita
                    if enemies[row][column].x <= 0:
                        enemy_direction = 1
                        inverted = True  # Altera direção para esquerda
                    elif enemies[row][column].x + enemies[row][column].width >= window.width:
                        enemy_direction = -1
                        inverted = True


def bullet_ship_collision():
    """
    Verifica se os disparos colidiram com alguma nave
    """

    # Acessando variável global
    global GAME_STATE
    global vidaVar

    # Para cada instância dos disparos
    for b in bullets:
        # Se for disparo do jogador
        if b.direction == -1:
            # Verifica se bateu em algum inimigo
            check_enemy_collision(b)

        # Se for disparo do inimigo
        elif b.direction == 1:
            # Verifica se bateu no jogador
            if b.collided(player):
                # Se bateu no jogador, define o fim de jogo
                vidaVar-=1
                bullets.remove(b)
                if vidaVar<=0:
                	GAME_STATE = 2
                	restart_window()


def check_enemy_collision(b):
    """
    Verifica se o projétil colidiu com o inimigo
    :param b: Instância de projétil
    """

    # Percorre toda a matriz de inimigos
    for row in range(matrix_x):
        for column in range(matrix_y):
            if enemies[row][column] != 0:
                # Se o inimigo ainda estiver vivo (enemies<div class="row"></div><div class=""></div> != 0),
                # verifica se o disparo b colidiu com o mesmo
                if b.collided(enemies[row][column]):
                    boom.set_position(b.x, b.y-30)
                    boom.unhide()
                    boom.play()


                    bullets.remove(b)



                    enemies[row][column] = 0
                    player.score +=100*difficulty
                    return


def bullet_bullet_collision():
    """
    Verifica se o projétil colidiu com alguma outro projétil
    """

    # Para cada instância de projétil
    for b1 in bullets:
        # Se for projétil do jogador
        if b1.direction == -1:
            # Verifica em todas as instâncias se ele colidiu com outro
            for b2 in bullets:
                # Verifica se o projétil atual é inimigo
                if b2.direction == 1:
                    # Se for inimigo, verifica se existiu colisão
                    if b1.collided(b2):
                        # Se houver colisão, remove os dois projéteis
                        bullets.remove(b1)
                        bullets.remove(b2)

                        break


def draw():
    """
    Desenha todos os elementos na tela
    """
    if boom.get_curr_frame() >= 11:
        boom.stop()
        boom.hide()

    boom.update()

    # Desenha todas as instâncias de projétil
    for b in bullets:
        b.draw()
        b.update()

    # Percorre todo a matriz de inimigos
    for row in range(matrix_x):
        for column in range(matrix_y):
            # Se o inimigo estiver vivo (!=0), desenha o inimigo
            if enemies[row][column] != 0:
                enemies[row][column].draw()
                enemies[row][column].update()
    window.draw_text("VIDA: "+str(vidaVar), 0, 0, 28, (255, 255, 255), "Calibri")
    boom.draw()

    # Desenha a nave do jogador


    player.draw()

def mouseMenu(button):
    if button.x <= mousepos[0] <= button.x + button.width and button.y <= mousepos[1] <= button.y + button.height:
        return True


def start_window():
    """
    Janela inicial do jogo
    """


    # Escreve o texto que informa as opções do jogador na tela
    window.draw_text("ENTER para jogar | ESC para sair", 0, 0, 28, (255, 255, 255), "Calibri")

    # Se jogador pressionou 'enter', inicia o jogo
    if keyboard.key_pressed("ENTER"):
        # Define a variável como 1, que significa que a partida está ativa
        GAME_STATE = 1
        # Reinicia o jogador, os inimigos e os disparos
        restart(player, enemies, bullets)

    # Se jogador pressionou 'esc', sai do jogo
    elif keyboard.key_pressed("ESCAPE"):
        window.close()


def restart_window():
    """
    Reinicia o jogo
    """

    # Acessando variável global
    global GAME_STATE
    global vidaVar

    # Escreve na tela a pontuação do jogador
    window.draw_text("Sua pontuação foi:" + str(player.score), 5, 5, 16, (255, 255, 255), "Calibri", True)

    # Quando o jogador pressionar 'enter', reinicia o jogo
    if keyboard.key_pressed("ENTER"):
        # Modifica o estado do jogo para 1, que significa partida ativa
        GAME_STATE = 0
        vidaVar = 3
        # Reinicia o jogador, os inimigos e os disparos
        restart(player, enemies, bullets)
cont=0
texto = "-"

menuFade = Sprite("Imagens/MENU.png")
play = Sprite("Imagens/play0.png")
settings = Sprite("Imagens/setti0.png")
score = Sprite("Imagens/score0.png")
exit = Sprite("Imagens/exit0.png")

menuFade.set_position(width/2 - menuFade.width/2, height/2 - menuFade.height/2)
play.set_position(menuFade.x, menuFade.y)
settings.set_position(menuFade.x, menuFade.y + play.height)
score.set_position(menuFade.x, menuFade.y + play.height + settings.height - 9)
exit.set_position(menuFade.x, menuFade.y + play.height + settings.height + score.height - 9)

while True:
    # Apaga a tela completamente
    window.set_background_color(background_color)

    scrolling(background_01, background_02, background_roll_speed)

    cont +=1
    if cont>100:
        cont =0
        texto = str(int(1/window.delta_time()))
    if window.delta_time()>0 and FPS ==True:
        window.draw_text("FPS: " + texto, 5, window.height-30, 18, (255, 255, 255), "DejaVu Sans Condensed", True)
        title = 'Space Invaders - ' + "FPS: " + texto

    mousepos = mouse.get_position()

    # Se o estado de jogo for = 0, quer dizer que é a primeira
    # vez que o game loop é acionado. Logo, ele cria a janela do
    # jogo.
    if GAME_STATE == 0:
        menuFade.draw()

        if mouseMenu(exit):
            exit.draw()
            if mouse.is_button_pressed(1):
                pygame.quit()

        if mouseMenu(play):
            play.draw()
            if mouse.is_button_pressed(1):
                GAME_STATE = 1
                restart(player, enemies, bullets)
                #start_window()
        if mouseMenu(settings):
            settings.draw()
            if mouse.is_button_pressed(1):
                GAME_STATE = 4
        if mouseMenu(score):
            score.draw()
            if mouse.is_button_pressed(1):
                GAME_STATE = 3
    # Se não for a primeira vez, quer dizer que a partida ainda
    # está acontecendo.
    elif GAME_STATE == 1:


        # Verifica se o jogador venceu a partida
        win()
        window.draw_text("STAGE: " + str(fase), width/2 - 15, 20, 18, (255, 255, 255), "DejaVu Sans Condensed", True)

        # Atualiza os contadores
        update_counters()

        # Atualiza a movimentação do jogador
        player_movement()

        # Controle os tiros a cada intervalo
        player_shoot()

        # Atualiza o movimento dos disparos
        bullet_movement()

        # Atualiza o movimento dos inimigos
        enemy_movement()

        # Verifica a colisão de projéteis contra naves
        bullet_ship_collision()

        # Verifica colisões entre projéteis
        bullet_bullet_collision()

        if player.score > highscore:
            highscore = player.score
        ## Renderiza todos os dados na tela ##
        draw()

    # Caso o jogo tenha terminado (GAME_STATE = 2), reinicia
    # a partida do jogo.
    elif GAME_STATE == 2:
        restart_window()
    elif GAME_STATE == 3:
        window.draw_text("Highscores:", width/4, 0, 48, (255, 255, 255), "Calibri")
        window.draw_text(str(highscore), width/4, height/4, 56, (255, 255, 255), "Calibri")

        # Se jogador pressionou 'enter', inicia o jogo
        if keyboard.key_pressed("ENTER") or keyboard.key_pressed("ESCAPE"):
            # Define a variável como 1, que significa que a partida está ativa
            GAME_STATE = 0

    elif GAME_STATE == 4:
        window.draw_text("Difficulty: " + str(difficulty), width/4, 0, 48, (255, 255, 255), "Calibri")
        window.draw_text("1     2      3", width/6, height/4, 130, (255, 255, 255), "Calibri")

        # Se jogador pressionou 'enter', inicia o jogo
        if keyboard.key_pressed("ENTER") or keyboard.key_pressed("ESCAPE"):
            # Define a variável como 1, que significa que a partida está ativa
            GAME_STATE = 0

        if mouse.is_button_pressed(1):
            if mousepos[0] <= width/3:
                difficulty =1
            elif mousepos[0] <= 2 * width/3:
                difficulty = 2
            else:
                difficulty = 3
    #print(difficulty)



    # Atualiza a janela de jogo cada vez que o game loop roda
    window.update()
