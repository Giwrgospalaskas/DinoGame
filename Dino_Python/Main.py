import pygame
import os
import random
import math

class Player():
    def __init__(self):
        self.jumping = False
        self.ducking = False
        self.posx = 60
        self.posy = 405
        self.alive =True
        #self.rect = pygame.Rect(60,450,20,40)
        self.jumpImg = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
        self.runImg = [pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")), pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png"))]
        self.duckImg = [pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")), pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png"))]
        self.deadImg = pygame.image.load(os.path.join("assets/Dino", "DinoDead.png"))
        self.image = self.runImg[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.posx
        self.rect.y = self.posy
        self.jumpingHeight = 24
        self.step = 0
        self.gravity = 1.7
        self.jumpForce = self.jumpingHeight
    
    def draw(self,screen):
        #pygame.draw.rect(screen, (0,0,0), self.rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, userInput):
        if self.alive:
            if self.step >= 19:
                self.step = 0
            self.step += 1

            if userInput[pygame.K_SPACE] and not self.ducking:
                self.jumping = True
            if userInput[pygame.K_DOWN] and not self.jumping:
                self.ducking = True
            else:
                self.ducking = False
            
            if self.jumping:
                self.jump()

            elif self.ducking:
                self.duck()

            else:
                self.run()
        else:
            self.dead()
    
    
    def jump(self):
        self.image = self.jumpImg
        self.rect.y -= self.jumpForce
        self.jumpForce -= self.gravity
        if self.jumpForce < -self.jumpingHeight:
            self.jumpForce = self.jumpingHeight
            self.jumping = False

    def run(self):
        self.image = self.runImg[self.step // 10]
        self.rect = self.image.get_rect()
        self.rect.y = self.posy
        self.rect.x = self.posx
    
    def duck(self):
        self.image = self.duckImg[self.step // 10]
        self.rect = self.image.get_rect()
        self.rect.y = self.posy + 32
        self.rect.x = self.posx

    def dead(self):
        self.image = self.deadImg

    def reset(self):
        self.jumping = False
        self.ducking = False
        self.step = 0
        self.jumpForce = self.jumpingHeight
        self.rect.x = self.posx
        self.rect.y = self.posy
        self.alive = True


class Ground():
    def __init__(self):
        self.image1 = pygame.image.load(os.path.join("assets/Ground", "Track.png"))
        self.image2 = pygame.image.load(os.path.join("assets/Ground", "Track.png"))
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect1.y = 470
        self.rect2.y = 470
        self.rect1.x = 0
        self.rect2.x = self.rect1.width - 3
    
    def draw(self,screen):
        screen.blit(self.image1, (self.rect1.x, self.rect1.y))
        screen.blit(self.image2, (self.rect2.x, self.rect2.y))

    def update(self,speed):
        if self.rect1.x <= -self.rect1.width:
            self.rect1.x = 0
            self.rect2.x = self.rect1.width - 2
        
        self.rect1.x -= speed
        self.rect2.x -= speed

    def reset(self):
        self.rect1.x = 0
        self.rect2.x = self.rect1.width - 3

class Obstacle():
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.alive = True
        self.rect.x = 960
    
    def update(self,speed):
        if self.alive:
            self.rect.x -= speed
    
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class LargeCactus(Obstacle):
    def __init__(self):
        self.posy = 395
        self.image = [pygame.image.load(os.path.join("assets/Obstacles/LargeCactus", "LargeCactus1.png")), pygame.image.load(os.path.join("assets/Obstacles/LargeCactus", "LargeCactus2.png")),pygame.image.load(os.path.join("assets/Obstacles/LargeCactus", "LargeCactus3.png"))]
        self.option = random.randint(0,2)
        self.obstacle = self.image[self.option]
        super().__init__(self.obstacle)
        self.rect.y = self.posy

class SmallCactus(Obstacle):
    def __init__(self):
        self.posy = 420
        self.image = [pygame.image.load(os.path.join("assets/Obstacles/SmallCactus", "SmallCactus1.png")), pygame.image.load(os.path.join("assets/Obstacles/SmallCactus", "SmallCactus2.png")),pygame.image.load(os.path.join("assets/Obstacles/SmallCactus", "SmallCactus3.png"))]
        self.option = random.randint(0,2)
        self.obstacle = self.image[self.option]
        super().__init__(self.obstacle)
        self.rect.y = self.posy


class Bird(Obstacle):
    def __init__(self):
        self.height = [412, 345, 303]
        self.option = random.choice(self.height)
        self.flyImg = [pygame.image.load(os.path.join("assets/Obstacles/Bird", "Bird1.png")), pygame.image.load(os.path.join("assets/Obstacles/Bird", "Bird2.png"))]
        self.image = self.flyImg[0]
        self.flap = 0
        super().__init__(self.image)
        self.rect.y = self.option
    
    
    def update(self,speed):
        if self.alive:
            if self.flap >= 19:
                self.flap = 0
            self.image = self.flyImg[self.flap // 10]
            self.flap += 1
            self.rect.x -= speed + 2
        else:
            self.image = self.flyImg[self.flap // 10]

class Score():
    def __init__(self):
        self.score = 0
        self.alive = True
        self.font = pygame.font.Font("assets/Fonts/PublicPixel.ttf", 16)
        self.color = (0,0,0)
        self.pos = (750, 20)
        self.text = self.font.render(f"Score: {self.score}", True, self.color)
    
    def update(self,speed):
        if self.alive:
            self.score += speed*0.023
        self.text = self.font.render(f"Score: {math.floor(self.score)}", True, self.color)

    def draw(self,screen):
        screen.blit(self.text, self.pos)

    def reset(self):
        self.score = 0
        self.alive = True

class RestartButton():
    def __init__(self):
        self.image = pygame.image.load(os.path.join("assets/Other", "Reset.png"))
        self.rect = self.image.get_rect()
        self.rect.x = 458
        self.rect.y = 200
        self.visible = False
        self.pos = (458,200)
    
    def show(self, screen):
        if self.visible:
            screen.blit(self.image, self.pos)

class Background():
    def __init__(self):
        self.cloud1 = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))
        self.cloud2 = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))
        self.cloud3 = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))
        self.posx1 = 960
        self.posx2 = 1300
        self.posx3 = 1700

    def draw(self,screen):
        screen.blit(self.cloud1, (self.posx1,120))        
        screen.blit(self.cloud2, (self.posx2,200))        
        screen.blit(self.cloud3, (self.posx3,160))

    def update(self,speed):
        if self.posx3 <= -self.cloud3.get_width():
            self.posx1 = 960
            self.posx2 = 1300
            self.posx3 = 1700
        

        self.posx1 -= speed
        self.posx2 -= speed
        self.posx3 -= speed

    def reset(self):
        self.posx1 = 960
        self.posx2 = 1300
        self.posx3 = 1700





def main():
    #window information
    displayHeight = 540 
    displayWidth = 960
    pygame.init()
    pygame.font.init()
    backgroundColor = (255,255,255)
    screen = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption("Dino Game")
    screen.fill(backgroundColor)
    pygame.display.flip()

    #Clock
    clock = pygame.time.Clock()
    running = True
    userInput = None
    initialSpeed = 10
    gameSpeed = initialSpeed
    speedIncrease = 0.009
    player = Player()
    ground = Ground()
    score = Score()
    restartButton = RestartButton()
    background = Background()
    obstacles = []
    collide = False
    font = pygame.font.Font("assets/Fonts/PublicPixel.ttf", 30)
    gameOvertxt = font.render("Game Over", True, (0,0,0))
    gameOverRect = gameOvertxt.get_rect()

    while running:
        clock.tick(60)  #Eixa xexasei na balw to roloi :/
        screen.fill(backgroundColor)
        #mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

        
        userInput = pygame.key.get_pressed()

        if len(obstacles) == 0:
            option = random.randint(0,2)
            if option == 0:
                obstacles.append(SmallCactus())
            elif option == 1:
                obstacles.append(LargeCactus())
            elif option == 2:
                obstacles.append(Bird())
                
        
        for obstacle in obstacles:
            obstacle.update(gameSpeed)
            obstacle.draw(screen)
            if obstacle.rect.x <= -obstacle.rect.width:
                obstacles.pop(0)
            collide = pygame.Rect.colliderect(obstacle.rect, player.rect)
        
        if collide:
            player.alive = False
            for obstacle in obstacles:
                obstacle.alive = False
            score.alive = False
            screen.blit(gameOvertxt, (360 ,100))
            restartButton.visible = True
            mouse = pygame.mouse.get_pos()
            if restartButton.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameSpeed = initialSpeed
                restartButton.visible = False
                player.reset()
                ground.reset()
                score.reset()
                for obstacle in obstacles:
                    del obstacle
                obstacles.pop()

        
        else:
            score.update(gameSpeed)
            player.update(userInput)
            ground.update(gameSpeed)
            background.update(gameSpeed)
            gameSpeed += speedIncrease

        background.draw(screen)
        restartButton.show(screen)
        score.draw(screen)
        ground.draw(screen)
        player.draw(screen)
        pygame.display.update()
    
    

if __name__ == "__main__":
    main()


