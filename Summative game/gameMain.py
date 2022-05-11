"""
Name: kevin li
Date: 17/4/18
Description: Space Shooters(bullet hell)
"""
# I - IMPORT AND INITIALIZE
import pygame, gameSprite, random, time
pygame.init()

def main():
    '''This function defines the 'mainline logic' for the Space shooters'''
      
    # DISPLAY
    #Sets the screen resolution and the name of the game   
    pygame.display.set_caption("Space shooters")
    screen = pygame.display.set_mode((640, 480))
    
    # ENTITIES
    #setting the moving background and music of the game
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background = pygame.image.load("space.jpeg")
    
    movingBackground = gameSprite.Space(screen)
    
    gameOver = pygame.image.load("youLose.png")
    gameOver = gameOver.convert()
   
    pygame.mixer.music.load("PETIT BISCUIT - Sunset Lover.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    #sound effects of an explosion sound of enemies dying or colliding with player
    explosion = pygame.mixer.Sound("explosionSound.wav")
    explosion.set_volume(0.15)
    #sound effects when the player shoots(when a bullet is created for the player)
    shootingSound = pygame.mixer.Sound("laserBlast.wav")
    shootingSound.set_volume(0.1)    
    
    # Sprites for: ScoreKeeper label, Player1, enemies, bullets, invisible sprites.
    player1 = gameSprite.PlayerSpaceship(screen, 1)
    mothership = gameSprite.Mothership(screen, 30)
    bullets = []
    scoreKeeper = gameSprite.ScoreKeeper()
    bombGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    bulletGroup = pygame.sprite.Group(bullets)
    powersGroup = pygame.sprite.Group()
    invisibleHandGroup = pygame.sprite.Group()
    #creating TheHands in the game to alster the direction of the Minions and updateing the allsprites
    for invisible in range(5):
        hand = gameSprite.TheHand(screen)
        invisibleHandGroup.add(hand)
    allSprites = pygame.sprite.OrderedUpdates(movingBackground, scoreKeeper, invisibleHandGroup, mothership, player1)
#ACTION    
    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
    counter = 0
    bulletCounter = 0
    monster = 0
    deadCounter = 0
    dead = 0
    totalMonster = 0
    fireSpeed = 10
    bulletDamage = 1
    changeBullet = 0
    mothershipValue = mothership.score()
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(30)
     
        # EVENT HANDLING: Player 1 uses arrow keys, player bullet shooting, creating Minions, enemy shooting, check if game is over, and collision detections
       
        #when the bulletCounter reaches a certain amount of time then it will degrade the value of the firespeed down by 1
        bulletCounter += 1
        if bulletCounter >= 1000:
            fireSpeed += 1
            bulletCounter = 0
         #counter will control the time when each bullet is created
        counter += 1    
        if counter >= fireSpeed and changeBullet == 0:
            shootingSound.play()
            bullet = gameSprite.Bullet(screen, player1.rect.centerx, player1.rect.centery + 20)
            bulletGroup.add(bullet)
            allSprites = pygame.sprite.OrderedUpdates(movingBackground, scoreKeeper, invisibleHandGroup, bulletGroup, mothership, player1, enemyGroup, powersGroup, bombGroup)
            counter = 0
            changeBullet = 1
        if counter >= fireSpeed and changeBullet == 1:
            shootingSound.play()
            bullet2 = gameSprite.Bullet2(screen, player1.rect.centerx, player1.rect.centery + 20)
            bulletGroup.add(bullet2)
            allSprites = pygame.sprite.OrderedUpdates(movingBackground, scoreKeeper, invisibleHandGroup, bulletGroup, mothership, player1, enemyGroup, powersGroup, bombGroup)
            counter = 0
            changeBullet = 0      
        #enemies will be created when the previous wave of enemies are all kill. it will start off with 2 enemies
        if deadCounter == dead:
            dead = 0
            deadCounter += 2
            if monster < 10:
                monster += 2 
                totalMonster = 0
            for mobs in range(monster):
                enemy = gameSprite.Minions(screen, 10)
                enemyGroup.add(enemy)
            value = enemy.score()
            allSprites = pygame.sprite.OrderedUpdates(movingBackground, scoreKeeper, invisibleHandGroup, bulletGroup, mothership, player1, enemyGroup, powersGroup, bombGroup)
        
        #this will randomize which enemies will shoot and will create enemy bullets on the Minions 
        for enemyShoot in enemyGroup:
            if random.randint(0, 100) == 7:
                shootingSound.play()
                bomb = gameSprite.EnemyBullet(screen, enemyShoot.rect.centerx, enemyShoot.rect.centery, player1.rect.centerx, player1.rect.centery)
                bombGroup.add(bomb)
                allSprites = pygame.sprite.OrderedUpdates(movingBackground, scoreKeeper, invisibleHandGroup, bulletGroup, mothership, player1, enemyGroup, powersGroup, bombGroup)        
        #checks to see if the player lost or quitted    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if scoreKeeper.loser() == 1:
                keepGoing = False  
                
            #player movement detection
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.change_direction((1.25, 0))
                if event.key == pygame.K_RIGHT:
                    player1.change_direction((-1.25, 0))
                if event.key == pygame.K_UP:
                    player1.change_direction((0,1.25))
                if event.key == pygame.K_DOWN:
                    player1.change_direction((0,-1.25))   
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player1.change_direction((-1.25, 0))
                if event.key == pygame.K_RIGHT:
                    player1.change_direction((1.25, 0))
                if event.key == pygame.K_UP:
                    player1.change_direction((0,-1.25))
                if event.key == pygame.K_DOWN:
                    player1.change_direction((0,1.25))
                    
        #Collision detection of player and mothership           
        if player1.rect.colliderect(mothership):
            explosion.play()
            mothership.getHit(bulletDamage)
            scoreKeeper.player1Damaged(2)
            if mothership.HP() <= 0:
                scoreKeeper.pointScored(mothershipValue)
                mothership.kill()
                mothership.reset()
                
        #collsion detection for player bullets and mothership. 
        if pygame.sprite.spritecollide(mothership, bulletGroup, False):
            for bBullet in bulletGroup:
                if bBullet.rect.colliderect(mothership):
                    explosion.play()
                    bBullet.kill()
                    mothership.getHit(bulletDamage)
                    # if the mothership dies then it will create powerups when randomPower2 = 0
                    if mothership.HP() <= 0:
                        randomPower2 = random.randint(0, 5)
                        if randomPower2 == 0:
                            powerUp = gameSprite.PowerUp(screen, mothership.rect.centerx, mothership.rect.centery)
                            powersGroup.add(powerUp)
                            allSprites = pygame.sprite.OrderedUpdates(movingBackground, scoreKeeper, invisibleHandGroup, bulletGroup, mothership, player1, enemyGroup, powersGroup, bombGroup)     
                            scoreKeeper.pointScored(mothershipValue)
                            mothership.kill()
                            mothership.reset()                             
                        else:
                            mothership.kill()
                            mothership.reset() 
                            scoreKeeper.pointScored(mothershipValue)
        #powerup will increase firespeed by 2 and will limit it so that it cannot be faster than 3 or lower
        for power in powersGroup:
            if player1.rect.colliderect(power):
                power.kill()
                if fireSpeed > 3:
                    fireSpeed -= 2
        #checks the collision between player1 and the enemygroup. score will increase by 10 each time a enemy is destroyed
        if pygame.sprite.spritecollide(player1, enemyGroup, False):
            for enemyTouch in pygame.sprite.spritecollide(player1, enemyGroup, False):
                explosion.play()
                scoreKeeper.pointScored(value)                
                enemyTouch.kill()
                enemyTouch.remove()
                scoreKeeper.player1Damaged(1)
                dead += 1  
                totalMonster += 1
        #collsion detection for the player1 and the enemybullets. if they collide than the player takes damage and the bullet is destroyed
        if pygame.sprite.spritecollide(player1, bombGroup, False):
            for enemyBullet in pygame.sprite.spritecollide(player1, bombGroup, False):
                explosion.play()
                scoreKeeper.player1Damaged(1)
                enemyBullet.kill()
        #this makes the enemys move in random directions if TheHand collides with the enemy Minions
        for hands in invisibleHandGroup:
            for enemyCounter in enemyGroup:
                if hands.rect.colliderect(enemyCounter.rect):
                    enemyCounter.changeDirection()
        #collsion detection between the all the players bullets and all the minions.            
        for bullet in bulletGroup:
            for enemyCounter in enemyGroup:
                if bullet.rect.colliderect(enemyCounter.rect):
                    explosion.play()
                    value2 = enemyCounter.score()
                    scoreKeeper.pointScored(value2)                    
                    enemyCounter.kill()
                    enemyCounter.remove()
                    bullet.kill()
                    dead += 1 
                    totalMonster += 1
                    #if the requirements are met then it will create a powerup at the destroyed minion
                    randomPower = random.randint(0, 20)
                    if randomPower == 0:
                        powerUp = gameSprite.PowerUp(screen, enemyCounter.rect.centerx, enemyCounter.rect.centery)
                        powersGroup.add(powerUp)
                        allSprites = pygame.sprite.OrderedUpdates(movingBackground, scoreKeeper, invisibleHandGroup, bulletGroup, mothership, player1, enemyGroup, powersGroup, bombGroup)                    
           
        # REFRESH SCREEN
        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
        
    #the game over image is blitted on the screen when the game is over and will delay it for 3 secs
    screen.blit(gameOver, (0,0))
    pygame.display.flip()
    time.sleep(3)     
    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)     
 
    # Close the game window
    pygame.quit()     
     
# Call the main function
main()        