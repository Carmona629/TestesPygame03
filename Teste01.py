import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

#Diretórios
dir_principal = os.path.dirname(__file__)
dir_imagens = os.path.join(dir_principal, "Imagens")
dir_sons = os.path.join(dir_principal, "sons")

pygame.init()
pygame.mixer.init()

#Cores
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 2555)
preto = (0, 0, 0)
branco = (255, 255, 255)

#Parâmetros tela
nome_da_tela = "DinoGame"
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption(nome_da_tela)
relogio = pygame.time.Clock()
FPS = 60

#carregar sprites
sprite_sheet = pygame.image.load(os.path.join(dir_imagens, "dinoSpritesheet.png")).convert_alpha()

#Sons
som_colisao = pygame.mixer.Sound(os.path.join(dir_sons, "death_sound.wav"))
som_colisao.set_volume(0.5)
colidiu = False

som_pontuacao = pygame.mixer.Sound(os.path.join(dir_sons, "score_sound.wav"))
som_pontuacao.set_volume(0.5)

escolha_obstaculo = choice([0, 1])
pontos = 0
velocidade = 10

#Classes e funções
def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont("arial", tamanho, True, False)
    mensagem = f"{msg}"
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade, colidiu, escolha_obstaculo
    pontos = 0
    velocidade = 10
    colidiu = False
    dino.rect.y = altura - 64 - (96 // 2)
    dino.pulo = False
    cacto.rect.x = largura
    galinha.rect.x = largura
    escolha_obstaculo = choice([0, 1])


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(dir_sons, "jump_sound.wav"))
        self.som_pulo.set_volume(0.5)

        self.imagens_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = altura - 64 - (96 // 2)
        self.rect.center = (100, self.pos_y_inicial)

        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 10
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 10
            else:
                self.rect.y = self.pos_y_inicial

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = largura - randrange(30, 660, 180)

    def update(self): #Faz o objeto se mover na tela
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= velocidade

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 64
        self.rect.x = pos_x * 64

    def update(self): #Faz o objeto se mover na tela
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (largura, altura - 64)
        self.rect.x = largura

    def update(self): #Faz o objeto se mover na tela
        if escolha_obstaculo == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade

class GalinhaVoadora(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.imagens_galinha = []
        for i in range(3, 5):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_galinha.append(img)

        self.index_lista = 0
        self.image = self.imagens_galinha[self.index_lista]
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (100, 300)
        self.rect.x = largura

    def update(self):
        if escolha_obstaculo == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade
            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_galinha[int(self.index_lista)]

#Criando objetos
todas_as_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
#Dino
dino = Dino()
todas_as_sprites.add(dino)
#Nuvem
for i in range(6):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

#Chão
    for i in range((largura // 64) + 1):
        chao = Chao(i)
        todas_as_sprites.add(chao)

#Cacto
cacto = Cacto()
todas_as_sprites.add(cacto)
obstaculos.add(cacto)

#Galinha voadora
galinha = GalinhaVoadora()
todas_as_sprites.add(galinha)
obstaculos.add(galinha)

while True:
    relogio.tick(FPS)
    tela.fill(branco)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key  == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()
            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(dino, obstaculos, False, pygame.sprite.collide_mask)

    todas_as_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or galinha.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        cacto.rect.x = largura
        galinha.rect.x = largura
        cacto.escolha = escolha_obstaculo
        galinha.escolha = escolha_obstaculo

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True
    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1
        game_over = exibe_mensagem("GAME OVER", 40, preto)
        tela.blit(game_over, (largura // 2, altura //2))
        restart = exibe_mensagem("Pressione r para reiniciar", 20, preto)
        tela.blit(restart, (largura //2, (altura // 2) + 45))
    else:
        pontos += 1
        todas_as_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 40, preto)

    if pontos % 100 == 0:
        som_pontuacao.play()
        if velocidade >= 20:
            velocidade += 0
        else:
            velocidade += 1

    tela.blit(texto_pontos, (520, 30))
    pygame.display.flip()