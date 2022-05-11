import pygame, random

class PlayerSpaceship(pygame.sprite.Sprite):
    '''This class defines the sprite for Player 1'''
    def __init__(self, screen, player_num):
        '''This initializer takes a screen surface. it will laod an image for that player and will position it at the center of the screen'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        # Define the image attributes for a black rectangle.
        self.__image = pygame.image.load("playerSpaceship.png")
        self.image = self.__image.convert()     
        self.image.set_colorkey((255,255,255))
        #self.__image2 = pygame.image.load("paddle-right.png")
        if player_num == 1:
            self.rect = self.image.get_rect()
            self.rect.centerx = 320
            self.rect.centery = 240        
            self.__dx = 0
            self.__dy = 0 
        else:
            pass

    def change_direction(self, xy_change):
        '''This method takes a (x,y) tuple as a parameter, extracts the 
        y element from it, and uses this to set the players y direction and the x direction.'''
        self.__dx += xy_change[0]
        self.__dy += xy_change[1]
    def update(self):
        '''This method will be called automatically to reposition the
        player sprite on the screen. it will check if the player is within the screen and will not allow the player to exit the screen'''
        # Check if we have reached the top or bottom of the screen.
        # If not, then keep moving the player in the same y direction.
        if ((self.rect.left > 0) and (self.__dx > 0)) or ((self.rect.right < self.__screen.get_width()) and (self.__dx < 0)):  
            self.rect.left -= (self.__dx*5)
            
        if ((self.rect.top > 0) and (self.__dy > 0)) or ((self.rect.bottom < self.__screen.get_height()) and (self.__dy < 0)):  
            self.rect.top -= (self.__dy*5)        
   
        # If yes, then we don't change the y position of the player at all.

class Bullet(pygame.sprite.Sprite):
    """the bullet interacts with other enemies in the game and is created on the player class"""
    def __init__(self, screen, x, y):
        """the init takes in the position of the player and will create a bullet at its position."""
        pygame.sprite.Sprite.__init__(self)
        self.__dx = 0
        self.__dy = 0
        self.__image = pygame.image.load("blueBullet.png")
        self.image = self.__image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y -40
    def update(self):
        """the bullets will travel upwards on the screen and if it exits the screen dimensions then it will be destroyed"""
        self.rect.top -= 10
        if (self.rect.left < 0) or (self.rect.top < 0) or (self.rect.right > 640) or (self.rect.bottom > 480):
            self.kill()
            
class Bullet2(pygame.sprite.Sprite):
    """the bullet interacts with other enemies in the game and is created on the player class"""
    def __init__(self, screen, x, y):
        """the init takes in the position of the player and will create a bullet at its position."""
        pygame.sprite.Sprite.__init__(self)
        self.__dx = 0
        self.__dy = 0
        self.__image = pygame.image.load("redBullet2.png")
        self.image = self.__image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y -40
    def update(self):
        """the bullets will travel upwards on the screen and if it exits the screen dimensions then it will be destroyed"""
        self.rect.top -= 10
        if (self.rect.left < 0) or (self.rect.top < 0) or (self.rect.right > 640) or (self.rect.bottom > 480):
            self.kill()
        
class Mothership(pygame.sprite.Sprite):
    """the mothership is a mini-boss that will give you 30 points when killed and comes down after a certian period of time"""
    def __init__(self, screen, value):
        """This takes a value from the main of what it is worth and has a set amount of healthpoints. it also sets its speed and direction and also sets the starting x value differently each time it is created or reseted."""
        self.__screen = screen
        pygame.sprite.Sprite.__init__(self)
        self.__image = pygame.image.load("bossShip.png")
        self.image = self.__image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,600)
        self.rect.centery = 0
        self.__health = 10
        self.__amount = value
        self.__dx = 0
        self.__dy = 2
    def getHit(self, damage):
        """When the player bullets hit the the mothership it will reduced its health by 1 healthpoint each time"""
        self.__health -= damage
    
    def HP(self):
        """We check the health of the mothership in the main to make sure it is dead or not when the health is below 1"""
        return self.__health
    
    def score(self):
        """When the mothership does die then it will return the valuye of how much it is worth to the main to add to the scoreboard"""
        return self.__amount
    
    def reset(self):
        """When the mothership dies, it will be reseted back to the desired y value so that will will come back down into the game screen fro the player to attempt to kill. This also sets the health of the mothership back to 3"""
        self.rect.centery = -1000
        self.__health = 10
    
    def update(self):
        """"The update will change the position of the mothership by a specific amount of pixels. it will also check if it has reached the bottom of the screen and if so then it will be reseted back up"""
        self.rect.bottom += (self.__dy)      
        if ((self.rect.top < 0) and (self.__dy < 0)) or ((self.rect.bottom > self.__screen.get_height() + 50) and (self.__dy > 0)):  
            self.rect.bottom = -1000
            self.__health = 10
            self.rect.centerx = random.randint(0,630)
                    
class Minions(pygame.sprite.Sprite):
    """This is a type of enemy that will offer 10 points when killed and does 1 damage to you if you touch it, it will spawn in random locations everytime it is created."""
    def __init__(self, screen, value):
        """The init will take in a value of what the minion is worth and moves at random directions and speeds"""
        self.__screen = screen
        pygame.sprite.Sprite.__init__(self)
        self.__image = pygame.image.load("minionBullet.png")
        self.image = self.__image.convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,640)
        self.rect.centery = random.randint(5, 20)
        self.__dx = random.randint(-5, 5)
        self.__dy = random.randint(-5, 5)
        self.__amount = value
        
    def score(self):
        """this will return a value back to the main where it will be added to the scoreboard"""
        return self.__amount
        
    def changeDirection(self):
        """When this is call, it will change the direction of the minion"""
        self.__dx = -self.__dx
    
    def update(self):
        """The position of the minion will increase/decrease by the dy/dx. it will also check if the minion is touching the screen boarders and if it does then it will move in the opposite direction"""
        self.rect.top += self.__dy
        self.rect.left += self.__dx
        if (self.rect.left <= 0) and (self.__dx < 0) or (self.rect.right >= 640) and (self.__dx > 0):
            self.__dx = -self.__dx
        if (self.rect.top <= 0) and (self.__dy < 0) or (self.rect.bottom >= 480) and (self.__dy > 0):
            self.__dy = -self.__dy        
    
class TheHand(pygame.sprite.Sprite):
    """TheHand will be colliding with the Minions so that the movement of the Minions are random"""
    def __init__(self, screen):
        """TheHand is invisible so the player cannot see it"""
        self.__screen = screen
        pygame.sprite.Sprite.__init__(self)
        self.__image = pygame.image.load("clearHand.png")
        self.image = self.__image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,630)
        self.rect.centery = random.randint(0, 480)
        self.__dx = random.randint(-5, 5)
        self.__dy = random.randint(-5, 5)
        
    def update(self):
        """This will update TheHand and will check if it does hit the screen boarders and if so then it will cause it to go the opposite direction"""
        self.rect.top += self.__dy
        self.rect.left += self.__dx
        if (self.rect.left <= 0) and (self.__dx < 0) or (self.rect.right >= self.__screen.get_width()) and (self.__dx > 0):
            self.__dx = -self.__dx
        if (self.rect.top <= 0) and (self.__dy < 0) or (self.rect.bottom >= self.__screen.get_height()) and (self.__dy > 0):
            self.__dy = -self.__dy
            
class PowerUp(pygame.sprite.Sprite):
    """When this calss is called from the main, a powerup will be created and placed at a specific point on the screen"""
    def __init__(self, screen, x, y):
        """This takes parameters of x and y of the minion so that when it dies, the power up will be created on the minions position"""
        self.__screen = screen
        pygame.sprite.Sprite.__init__(self)
        self.__dx = 0
        self.__dy = 3
        self.__image = pygame.image.load("powerUp.png")
        self.image = self.__image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y 
    def update(self):
        """This will make the powerup descend down the screen and if it is greater then the screen height then it will kill it self """
        self.rect.top += self.__dy
        if self.rect.top > self.__screen.get_height():
            self.kill()
        
class EnemyBullet(pygame.sprite.Sprite):
    """This sprite defines the enemy bullets that the minion class sprites shoot"""
    def __init__(self, screen, x1, y1, x2, y2):
        """This sets the bullets speed and direction, laods the image"""
        pygame.sprite.Sprite.__init__(self)
        #self.__damage = 1
        self.__dx =  (x2 - x1) / 30
        self.__dy = (y2 - y1) / 30
        self.__image = pygame.image.load("redBullet.png")
        self.image = self.__image.convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x1
        self.rect.centery = y1        
    def update(self):
        """This updates the bullets position everytime the update is called so that the bullet will look like it is moving"""
        self.rect.centerx += self.__dx
        self.rect.centery += self.__dy
        if (self.rect.left < 0) or (self.rect.top < 0) or (self.rect.right > 630) or (self.rect.bottom > 480):
            self.kill()        
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score and the lives.'''
    def __init__(self):
        '''This initializer loads the system font "Xanadu.ttf", and
        sets the starting lives to 3'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("Xanadu.ttf", 30)
        self.__lives = 3
        self.__score = 0
         
    def player1Damaged(self, healthLoss):
        '''This method subtracts one life from the lives if a ball hits the endzone'''
        self.__lives -= healthLoss
 
    def pointScored(self, value):
        '''This method adds the value of the brick that the ball collided with to the score total'''
        self.__score += value
     
    def loser(self):
        '''When the lives are at 0 then the game ends
        This method returns 0 if there is no loser yet, 1 if there is no move lives, it will return 1'''
        if self.__lives <= 0:
            return 1
        else:
            return 0
 
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        message = "Lives: %d Score %d" %\
                (self.__lives, self.__score)
        self.image = self.__font.render(message, 1, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 15)

class Space(pygame.sprite.Sprite):
    def __init__(self, screen):
            self.__screen = screen
            pygame.sprite.Sprite.__init__(self)
            self.__image = pygame.image.load("SpaceBackground.jpg")
            self.image = self.__image.convert()
            self.rect = self.image.get_rect()
            self.rect.bottom = 500
            self.rect.left = 0
            self.__dy = 1
    def update(self):
        self.rect.top += self.__dy
        if self.rect.top > 0:
            self.rect.bottom = 480