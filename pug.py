import pygame
import random


class Hero:
    """Класс героя"""
    def __init__(self, hero):
        self.__x = hero['hero']['width'] * 3
        self.__y = hero['game']['height'] - 118 - hero['hero']['height']
        self.__width = hero['hero']['width']
        self.__height = hero['hero']['height']
        self.__sprites = [pygame.image.load(i) for i in hero['hero']['sprites']]
        self.__jumpHeight = hero['hero']['jumpHeight']
        self.__jumpSprite = pygame.image.load(hero['hero']['jump'])
        self.__isJump = False
        self.__jumpSound = hero['hero']['jumpSound']
        self.__fallSound = hero['hero']['fallSound']
        self.__sprite = 0

    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    @property
    def width(self):
        return self.__width
    @property
    def height(self):
        return self.__height
    def run(self, display):
        if not self.__isJump:
            if self.__sprite >= len(self.__sprites):
                self.__sprite = 0
            display.blit(self.__sprites[self.__sprite], (self.__x, self.__y))
            self.__sprite += 1
        else:
            display.blit(self.__jumpSprite, (self.__x, self.__y))

    def jump(self, display):
        # Метод прыжка
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.__isJump = True
        if self.__isJump:
            if self.__jumpHeight[0] >= -self.__jumpHeight[1]:
                if self.__jumpHeight[0] == self.__jumpHeight[1]:
                    pygame.mixer.Sound.play(pygame.mixer.Sound(self.__jumpSound))
                if self.__jumpHeight[0] == -self.__jumpHeight[1] + 6:
                    pygame.mixer.Sound.play(pygame.mixer.Sound(self.__fallSound))
                self.__y -= self.__jumpHeight[0] / 0.7
                self.__jumpHeight[0] -= 2
            else:
                self.__jumpHeight[0] = self.__jumpHeight[1]
                self.__isJump = False

class Enemy:
    """Класс врага"""
    def __init__(self, enemy):
        self.__width = enemy['enemy']['width']
        self.__height = enemy['enemy']['height']
        self.__born = enemy['game']['width'] + self.__width
        self.__x = self.__width + enemy['game']['width']
        self.__y = enemy['game']['height'] - 100 - self.__height
        self.__sprite = pygame.image.load(enemy['enemy']['sprite'])
        self.__speed = enemy['enemy']['speed']

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def oncoming(self, display):
        if self.__x >= -self.__width - self.__height:
            display.blit(self.__sprite, (self.__x, self.__y))
            self.__x -= self.__speed
        else:
            self.__x = self.__born + random.randrange(self.__width, self.__born)


class Game:
    """Класс игры"""
    def __init__(self, game):

        self.__pug = Hero(game)
        self.__stone = Enemy(game)

        self.__width = game['game']['width']
        self.__height = game['game']['height']
        self.__display = pygame.display.set_mode((self.__width, self.__height))
        self.__FPS = game['game']['fps']
        self.__name = game['game']['name']
        self.__icon = game['game']['icon']
        self.__font = game['game']['font']

        self.__music = game['game']['music']
        self.__background = pygame.image.load(game['game']['background'])

        self.__backgroundMenu = pygame.image.load(game['game']['menu']['background'])
        self.__buttonUnpressed = pygame.image.load(game['game']['menu']['buttonUnpressed'])
        self.__buttonPressed = pygame.image.load(game['game']['menu']['buttonPressed'])
        self.__buttonX = 200
        self.__buttonY = 270
        self.__buttonWidth = 400
        self.__buttonHeight = 120

        self.__land = pygame.image.load(game['game']['land']['image'])
        self.__landWidth = game['game']['land']['width']
        self.__landHeight = game['game']['land']['height']
        self.__landX = 0
        self.__landY = self.__height - self.__landHeight

        self.__sun = pygame.image.load(game['game']['sun']['image'])
        self.__sunWidth = game['game']['sun']['width']
        self.__sunHeight = game['game']['sun']['height']
        self.__sunX = self.__width
        self.__sunY = 0

        self.__clouds = pygame.image.load(game['game']['clouds']['image'])
        self.__cloudsWidth = game['game']['clouds']['width']
        self.__cloudsHeight = game['game']['clouds']['height']
        self.__cloudsX = self.__width / 2
        self.__cloudsY = 280

        self.__point = pygame.image.load(game['game']['point']['image'])
        self.__pointWidth = game['game']['point']['width']
        self.__pointHeight = game['game']['point']['height']
        self.__pointX = self.__stone.x - self.__pointWidth
        self.__pointY = self.__height - 120 - self.__pointHeight
        self.__points = 0

        self.gameMenu()

    def printText(self, text, size, color, x, y):
        fontType = pygame.font.Font(self.__font, size)
        write = fontType.render(text, True, color)
        self.__display.blit(write, (x, y))

    def moveLand(self):
        if self.__landX >= -self.__landWidth + self.__width:
            self.__display.blit(self.__land, (self.__landX, self.__landY))
            self.__landX -= 12
        else:
            self.__landX = 0

    def moveSun(self):
        if self.__sunX >= self.__width/3:
            self.__display.blit(self.__sun, (self.__sunX, self.__sunY))
            self.__sunX -= 1
        else:
            self.__display.blit(self.__sun, (self.__sunX, self.__sunY))

    def moveClouds(self):
        if self.__cloudsX >= -self.__cloudsWidth :
            self.__display.blit(self.__clouds, (self.__cloudsX, self.__cloudsY))
            self.__cloudsX -= 2
        else:
            self.__cloudsX = self.__width + self.__cloudsWidth
    def isPoint(self):
        """"Метод опредления собран ли пончик"""
        if self.__pug.y + self.__pug.height >= self.__pointY:
            if self.__pointX <= self.__pug.x <= self.__pointX + self.__pointWidth:
                return True
            elif self.__pointX <= self.__pug.x + self.__pug.width - 30 <= self.__pointX + self.__pointWidth:
                return True
        else:
            return False
    def gameOver(self):
        """"Метод проигрыша"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.printText('камень на дороге', 30, (255, 185, 247), 50, 200)
            self.printText('нажмите Esc чтобы выйти из игры', 30, (255, 185, 247), 50, 250)
            self.printText('Всего собрано пончиков:' + str(self.__points), 30, (255, 185, 247), 50, 300)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                quit()
            pygame.display.flip()

        self.__points = 0
        pass
    def movePoint(self):
        """"Метод перемещения пончика"""
        if not self.isPoint() and self.__pointX >= 0:
            self.__display.blit(self.__point, (self.__pointX, self.__pointY))
            self.__pointX -= 12
        else:
            self.__pointX = self.__width

    def isCollision(self):
        """Метод проверки столкновения"""

        if self.__pug.y + self.__pug.height >= self.__stone.y + 18:
            if self.__stone.x <= self.__pug.x <= self.__stone.x + self.__stone.width:
                return True
            elif self.__stone.x <= self.__pug.x + self.__pug.width - 30 <= self.__stone.x + self.__stone.width:
                return True
        return False

    def render(self):
        """Метод прорисовки всех элементов"""

        self.__display.blit(self.__background, (0, 0))
        self.moveLand()
        self.moveSun()
        self.moveClouds()
        self.movePoint()
        self.__pug.run(self.__display)
        self.__pug.jump(self.__display)
        self.__stone.oncoming(self.__display)
        self.printText('пончиков:'+str(self.__points), 30, (255, 185, 247), 0, 0)
        pygame.display.flip()
    def setingsGame(self):
        pygame.display.set_caption(self.__name)
        icon = pygame.image.load(self.__icon)
        pygame.display.set_icon(icon)

    def gameMenu(self):
        pygame.init()
        self.setingsGame()
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  return
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            self.__display.blit(self.__backgroundMenu, (0, 0))
            if self.__buttonX < mouse[0] < self.__buttonX + self.__buttonWidth and self.__buttonY < mouse[1] < self.__buttonY + self.__buttonHeight:
                self.__display.blit(self.__buttonPressed, (self.__buttonX - 27, self.__buttonY - 27))
                if click[0] == 1:
                    self.runGame()
            else:
                self.__display.blit(self.__buttonUnpressed, (self.__buttonX, self.__buttonY))
            clock.tick(self.__FPS)
            pygame.display.update()

    def runGame (self):
        pygame.init()
        self.setingsGame()
        clock = pygame.time.Clock()
        pygame.mixer.music.load(self.__music)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        while True:
            clock.tick(self.__FPS)
            """Основной цикл игры"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if self.isCollision():
                self.gameOver()
            if self.isPoint():
                self.__points += 1
            if self.__points > 0 and self.__points % 30 == 0:
                self.__FPS += 1

            self.render()
        quit()

def main ():
    frFr = {'game':
                     {
                         'width': 800,
                         'height': 600,
                         'fps': 30,
                         'name': 'Фр-Фр',
                         'icon': 'icon.gif',
                         'font': 'font2.ttf',
                         'background': 'background.jpg',
                         'music': 'moon.mp3',
                         'land': {'width': 10000, 'height': 153, 'image': 'land.jpg'},
                         'sun': {'width': 269, 'height': 290, 'image': 'sun269x290.jpg'},
                         'clouds': {'width': 1000, 'height': 140, 'image': 'clouds.jpg'},
                         'point': {'width': 50, 'height': 50, 'image': 'donut.png'},
                         'menu': {'background': 'menu.jpg', 'buttonPressed': 'pressed.png', 'buttonUnpressed': 'unpressed.png'}
                     },
        'hero': {'width': 100, 'height': 57, 'sprites': ['pug-1.gif', 'pug-2.gif', 'pug-3.gif', 'pug-4.gif', 'pug-5.gif', 'pug-6.gif', 'pug-7.gif', 'pug-8.gif'], 'jumpHeight': [24, 24], 'jump': 'pug-6.gif', 'jumpSound': 'jump2.wav', 'fallSound': 'fall3.wav'},
        'enemy': {'width': 128, 'height': 72, 'sprite': 'stone70.png', 'speed': 12}
                 }

    game = Game(frFr)

if __name__ == '__main__':
    main()