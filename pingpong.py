import pygame, sys, random

# Setup geral
pygame.mixer.pre_init(44100, -16, 2, 800)
pygame.init()
clock = pygame.time.Clock()

def bola_animation():
    global bola_velocidade_y, bola_velocidade_x, jogador_score, jogador2_score, score_time

    bola.x += bola_velocidade_x
    bola.y += bola_velocidade_y

    if bola.top <= 0 or bola.bottom >= tela_altura:
        pygame.mixer.Sound.play(pong_som)
        bola_velocidade_y *= -1

    #Pontuação do jogador
    if bola.left <= 0:
        pygame.mixer.Sound.play(score_som)
        jogador_score +=1
        score_time = pygame.time.get_ticks()
        pygame.mixer.Sound.play(contagem_som)

    #pontuação do oponente
    if bola.right >= tela_largura:
        pygame.mixer.Sound.play(score_som1)
        jogador2_score +=1
        score_time = pygame.time.get_ticks()
        pygame.mixer.Sound.play(contagem_som)


    if bola.colliderect(jogador) and bola_velocidade_x > 0:
        pygame.mixer.Sound.play(pong_som)
        if abs(bola.right - jogador.left) <10:
            bola_velocidade_x *= -1
        elif abs(bola.bottom - jogador.top) < 10 and bola_velocidade_y > 0:
            bola_velocidade_y *= -1
        elif abs(bola.top - jogador.bottom) < 10 and bola_velocidade_y < 0:
            bola_velocidade_y *= -1

    if bola.colliderect(jogador2) and bola_velocidade_x < 0:
        pygame.mixer.Sound.play(pong_som)
        if abs(bola.left - jogador2.right) < 10:
            bola_velocidade_x *= -1
        elif abs(bola.bottom - jogador2.top) < 10 and bola_velocidade_y > 0:
            bola_velocidade_y *= -1
        elif abs(bola.top - jogador2.bottom) < 10 and bola_velocidade_y < 0:
            bola_velocidade_y *= -1

def jogador_animation():
    jogador.y += jogador_velocidade

    if jogador.top <= 0:
        jogador.top = 0
    if jogador.bottom >= tela_altura:
        jogador.bottom = tela_altura

def jogador2_ai():
    if jogador2.top < bola.y:
        jogador2.top += jogador2_velocidade
    if jogador2.bottom > bola.y:
        jogador2.bottom -= jogador2_velocidade

    if jogador2.top <= 0:
        jogador2.top = 0
    if jogador2.bottom >= tela_altura:
        jogador.bottom = tela_altura

def bola_restart():
    global bola_velocidade_y, bola_velocidade_x, score_time, score_fonte, score_fonte2

    current_time = pygame.time.get_ticks()
    bola.center = (tela_largura / 2, tela_altura / 2)

    if current_time - score_time < 700:
        numero_tres = score_fonte2.render('3', False, red)
        tela.blit(numero_tres, (tela_largura/2 - 25, tela_altura/2 - 200))
    if 700 < current_time - score_time < 1400:
        numero_dois = score_fonte2.render('2', False, red)
        tela.blit(numero_dois, (tela_largura/2 - 25, tela_altura/2 - 200))
    if 1400 < current_time - score_time < 2100:
        numero_um = score_fonte2.render('1', False, red)
        tela.blit(numero_um, (tela_largura/2 - 25, tela_altura/2 - 200))

    if current_time - score_time < 2100:
        bola_velocidade_x, bola_velocidade_y = 0,0
    else:
        bola_velocidade_y = 7 * random.choice((1, -1))
        bola_velocidade_x = 7 * random.choice((1, -1))
        score_time = None

# Configurando a janela principal
tela_largura = 1280
tela_altura = 960
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption('PingPong')

# Cores
light_grey = (200, 200, 200)
bg_color = pygame.Color('#2F373F')
accent_color = ((255,69,0))
red = (255, 255, 255)

# Retangulos do jogo
bola = pygame.Rect(tela_largura/2 - 15, tela_altura/2 - 15, 30, 30)
jogador = pygame.Rect(tela_largura - 20, tela_altura/2 -70, 10, 140)
jogador2 = pygame.Rect(10, tela_altura/2 - 70, 10, 140)

# Variaveis do jogo
bola_velocidade_x = 7 * random.choice((1, -1))
bola_velocidade_y = 7 * random.choice((1, -1))
jogador_velocidade = 0
jogador2_velocidade = 7

# Variaveis de texto
jogador_score = 0
jogador2_score = 0
score_fonte = pygame.font.Font('freesansbold.ttf', 32)
score_fonte2 = pygame.font.Font('freesansbold.ttf', 100)

# score time
score_time = True

# Som
pong_som = pygame.mixer.Sound('pong.mp3')
score_som = pygame.mixer.Sound('score.mp3')
score_som1 = pygame.mixer.Sound('score1.mp3')
contagem_som = pygame.mixer.Sound('contagem.mp3')

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                jogador_velocidade +=7
            if evento.key == pygame.K_UP:
                jogador_velocidade -=7
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_DOWN:
                jogador_velocidade -=7
            if evento.key == pygame.K_UP:
                jogador_velocidade +=7

    #Logica do jogo
    bola_animation()
    jogador_animation()
    jogador2_ai()

    #Visuais

    tela.fill(bg_color)
    pygame.draw.rect(tela, accent_color, jogador)
    pygame.draw.rect(tela, accent_color, jogador2)
    pygame.draw.ellipse(tela, light_grey, bola)
    pygame.draw.aaline(tela, light_grey, (tela_largura/2,0), (tela_largura/2, tela_altura))

    if score_time:
        bola_restart()

    jogador_texto = score_fonte.render(f'{jogador_score}', False, light_grey)
    tela.blit(jogador_texto, (665, 470))
    jogador2_texto = score_fonte.render(f'{jogador2_score}', False, light_grey)
    tela.blit(jogador2_texto, (595, 470))
    jogador_texto = score_fonte.render('Jogador', False, light_grey)
    tela.blit(jogador_texto, (900, 20))
    jogador2_texto = score_fonte.render('Computador', False, light_grey)
    tela.blit(jogador2_texto, (230, 20))

    #Atualizando a janela
    pygame.display.flip()
    clock.tick(75)
