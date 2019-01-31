#!/usr/bin/env python
# Team member: name: Mengde Wu netId: mw934
#              name: Yexiang Chang netId: yc2523

import sys
import pygame
from pygame.locals import *
import time
import cv2
import os
import numpy as np
from header import *

######################################## Initialization #########################################

# initialize pygame
pygame.init()
pygame.display.set_caption('PI AR GAME')

# set color
black = 0, 0, 0
green = 124, 252, 0
red = 255, 0, 0
blue = 0, 255, 255
yellow = 255, 215, 0
white = 255, 255, 255

# set the size of screen to 640*480
size = width, height = 640, 480
# initialize the screen with parameter size
screen = pygame.display.set_mode(size)

# load all images
map_image = pygame.transform.scale(pygame.image.load("map.jpg")\
                                        ,(120,120))
map_rect = map_image.get_rect(center=[width-80,80])

pi_image = pygame.transform.scale(pygame.image.load("pi.png")\
                                        ,(90,120))
pi_rect = pi_image.get_rect(center=[150,240])

ar_image = pygame.transform.scale(pygame.image.load("ar.png")\
                                        ,(90,120))
ar_rect = ar_image.get_rect(center=[260,240])

game_image = pygame.transform.scale(pygame.image.load("game.png")\
                                        ,(250,120))
game_rect = game_image.get_rect(center=[450,240])

hero_image = pygame.transform.scale(pygame.image.load("hero.png")\
					,(100,100))
hero_rect = hero_image.get_rect(center=[70,70])


sword_image = pygame.transform.scale(pygame.image.load("sword.png")\
					,(128,128))
spring_image = pygame.transform.scale(pygame.image.load("spring.png")\
					,(128,118))

atk_image = pygame.transform.scale(pygame.image.load('attack.png')\
                                        ,(100,100))

skill_image = pygame.transform.scale(pygame.image.load('skill.png')\
                                        ,(200,200))
skill_rect = skill_image.get_rect(center=[320,240])

dead_image = pygame.transform.scale(pygame.image.load('dead.png')\
                                        ,(300,300))
dead_rect = dead_image.get_rect(center=[320,240])

heal_image = pygame.transform.scale(pygame.image.load('heal.png')\
                                        ,(100,100))

skillbutton_image = pygame.transform.scale(pygame.image.load('skillbutton.png')\
                                        ,(100,30))

forward_image = pygame.transform.scale(pygame.image.load('forward.png')\
                                        ,(100,100))
forward_rect = forward_image.get_rect(center=[320,80])

backward_rect = forward_image.get_rect(center=[320,480-80])

left_image = pygame.transform.scale(pygame.image.load('right.png')\
                                        ,(100,100))

left_rect = left_image.get_rect(center=[70,480-70])

right_rect = left_image.get_rect(center=[640-70,480-70])

close_image = pygame.transform.scale(pygame.image.load('close.png')\
                                        ,(20,20))
close_rect = close_image.get_rect(center=[640-10,10])

# set font
my_font = pygame.font.Font(None, 20)

# initialize camera (using opencv, videocapture)
camera = cv2.VideoCapture(0)

############################# Drawing(virtual buttons; UI; Background) #####################################

display_mode = True

# draw the virtual buttons
def draw_movebutton():
    screen.blit(forward_image,forward_rect)
    screen.blit(pygame.transform.flip(forward_image, False, True),backward_rect)
    screen.blit(left_image,left_rect)
    screen.blit(pygame.transform.flip(left_image, True, False),right_rect)
  
# draw the ui of this game
def draw_ui():
    global pos, map_image,map_rect
    global map
    global name
    
    # show player lv and name
    screen.blit(map_image, map_rect)
    screen.blit(hero_image, hero_rect)
    
    ply_info = 'lv: '+str(player.lv)+'  '+name
    ply_button = {ply_info:(55,125),\
                  'HP: ':(35,145),\
                  'MP: ':(35,165),\
                  'EXP:':(35,185),\
                  'Death: '+str(player.death):(45,205),\
		          'Atk: '+str(player.atk):(40,225)}
    
    # show player hp
    pygame.draw.rect(screen,red,(20,\
                                 140,\
                                 100,
                                 10),0)
    pygame.draw.rect(screen,green,(20,\
                                 140,\
                                 player.hp,
                                 10),0)
    
    # show player mp
    pygame.draw.rect(screen,red,(20,\
                                 160,\
                                 100,
                                 10),0)
    pygame.draw.rect(screen,blue,(20,\
                                 160,\
                                 player.mp,
                                 10),0)
    
    # show player exp
    pygame.draw.rect(screen,red,(20,\
                                 180,\
                                 100,
                                 10),0)
    pygame.draw.rect(screen,yellow,(20,\
                                 180,\
                                 player.exp,
                                 10),0)
    
    for my_text, text_pos in ply_button.items():
        text_surface = my_font.render(my_text, True, white)
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
    
    if display_mode:
    	for i in range(5):
	    for j in range(5):
	    	if map[i+1,j+1] > 1 and map[i+1,j+1] <= 6:
                    pygame.draw.circle(screen, red, [560+(j+0-3)*24+24,\
                                                 80+(i+2-3)*24-24], 5)
	    	if map[i+1,j+1] == 7:
                    pygame.draw.circle(screen, blue, [560+(j+0-3)*24+24,\
                                                 80+(i+2-3)*24-24], 5)
	    	if map[i+1,j+1] == 8:
                    pygame.draw.circle(screen, green, [560+(j+0-3)*24+24,\
                                                 80+(i+2-3)*24-24], 5)			
    
    
    	arrow_image = pygame.transform.scale(pygame.image.load("arrow.png")\
                                        ,(20,20))
    	arrow_rotate = pygame.transform.rotate(arrow_image, 90*(pos[2]-1))
    	arrow_rect = arrow_rotate.get_rect(center=[560+(pos[1]-3)*24,80+(pos[0]-3)*24])
    	screen.blit(arrow_rotate, arrow_rect)

    else:
	
        arrow_image = pygame.transform.scale(pygame.image.load("arrow.png")\
                                        ,(20,20))
    	arrow_rotate = pygame.transform.rotate(arrow_image, 90*(2-1))
    	arrow_rect = arrow_rotate.get_rect(center=[560,80])

	    if pos[2] == 2:
    	    for i in range(5):
	    	for j in range(5):
	    	    if map[i+1,j+1] > 1 and map[i+1,j+1] <= 6:
                    	pygame.draw.circle(screen, red, [560+(j+0-3)*24+24,\
                                                 80+(i+2-3)*24-24], 5)
	    	    if map[i+1,j+1] == 7:
                    	pygame.draw.circle(screen, blue, [560+(j+0-3)*24+24,\
                                                 80+(i+2-3)*24-24], 5)
	    	    if map[i+1,j+1] == 8:
                    	pygame.draw.circle(screen, green, [560+(j+0-3)*24+24,\
                                                 80+(i+2-3)*24-24], 5)
	    elif pos[2] == 4:
    	    for i in range(5):
	    	for j in range(5):
	    	    if map[i+1,j+1] > 1 and map[i+1,j+1] <= 6:
                    	pygame.draw.circle(screen, red, [560+(4-j+0-3)*24+24,\
                                                 80+(4-i+2-3)*24-24], 5)
	    	    if map[i+1,j+1] == 7:
                    	pygame.draw.circle(screen, blue, [560+(4-j+0-3)*24+24,\
                                                 80+(4-i+2-3)*24-24], 5)
	    	    if map[i+1,j+1] == 8:
                    	pygame.draw.circle(screen, green, [560+(4-j+0-3)*24+24,\
                                                 80+(4-i+2-3)*24-24], 5)
	    elif pos[2] == 1:
    	    for i in range(5):
	    	for j in range(5):
	    	    if map[i+1,j+1] > 1 and map[i+1,j+1] <= 6:
                    	pygame.draw.circle(screen, red, [560+(i+0-3)*24+24,\
                                                 80+(4-j+2-3)*24-24], 5)
	    	    if map[i+1,j+1] == 7:
                    	pygame.draw.circle(screen, blue, [560+(i+0-3)*24+24,\
                                                 80+(4-j+2-3)*24-24], 5)
	    	    if map[i+1,j+1] == 8:
                    	pygame.draw.circle(screen, green, [560+(i+0-3)*24+24,\
                                                 80+(4-j+2-3)*24-24], 5)
	    elif pos[2] == 3:
    	    for i in range(5):
	    	for j in range(5):
	    	    if map[i+1,j+1] > 1 and map[i+1,j+1] <= 6:
                    	pygame.draw.circle(screen, red, [560+(4-i+0-3)*24+24,\
                                                 80+(j+2-3)*24-24], 5)
	    	    if map[i+1,j+1] == 7:
                    	pygame.draw.circle(screen, blue, [560+(4-i+0-3)*24+24,\
                                                 80+(j+2-3)*24-24], 5)
	    	    if map[i+1,j+1] == 8:
                    	pygame.draw.circle(screen, green, [560+(4-i+0-3)*24+24,\
                                                 80+(j+2-3)*24-24], 5)
	
    	screen.blit(arrow_rotate, arrow_rect)
    
    screen.blit(close_image,close_rect)

# draw the background of the game
def background():
    global screen,camera
    
    ret, frame = camera.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = np.fliplr(frame)
    frame = pygame.surfarray.make_surface(frame)
    
    # show background
    screen.blit(frame,(0,0))
    
    draw_ui()

# draw the monster (show what you are facing)    
def generate_monster(num,Center):
    if num == 2:
        monster = pygame.image.load(bat.pic)
        mon_rect = monster.get_rect(center=Center)
        screen.blit(monster,mon_rect)
    elif num == 3:
        monster = pygame.image.load(centaur.pic)
        mon_rect = monster.get_rect(center=Center)
        screen.blit(monster,mon_rect)
    elif num == 4:
        monster = pygame.image.load(angryboy.pic)
        mon_rect = monster.get_rect(center=Center)
        screen.blit(monster,mon_rect)
    elif num == 5:
        monster = pygame.image.load(pumpkin.pic)
        mon_rect = monster.get_rect(center=Center)
        screen.blit(monster,mon_rect)
    elif num == 6:
        monster = pygame.image.load(dragon.pic)
        mon_rect = monster.get_rect(center=Center)
        screen.blit(monster,mon_rect)
    elif num == 7:
        mon_rect = sword_image.get_rect(center=Center)
        screen.blit(sword_image,mon_rect)  
    elif num == 8:
        mon_rect = spring_image.get_rect(center=Center)
        screen.blit(spring_image,mon_rect)  

###################################### BATTLING #########################################

# the main function when you encounter a monster
def encountering_monster(Monster):
    global flag

    pygame.mixer.music.load('encounter.ogg')
    pygame.mixer.music.play(-1)

    full_hp = Monster.hp
    mon_image = pygame.transform.scale(pygame.image.load(Monster.pic)\
                                        ,(160,160))
    mon_rect = mon_image.get_rect(center=[320,240])
    speed = [1,1]
    
    start = time.time()
    
    while Monster.hp > 0 and flag:
        
        # monster hit player once per sec
        if time.time() - start > 1:
            player.hp -= Monster.atk

            start = time.time()
            if player.hp <= 0:
                player.hp = 100
                player.death += 1
                break
                
            background()
            
            atk_rect = atk_image.get_rect(center=[int(uniform(hero_rect.left,\
                                                              hero_rect.right)),\
                                                  int(uniform(hero_rect.top,\
                                                              hero_rect.bottom))])
            screen.blit(atk_image, atk_rect)
        
        else:
            background()
        
        skillbutton_rect = skillbutton_image.get_rect(center=[560,440])
        screen.blit(skillbutton_image, skillbutton_rect)
        
        skillbutton_rect = skillbutton_image.get_rect(center=[560,400])
        screen.blit(skillbutton_image, skillbutton_rect)

        skillbutton_rect = skillbutton_image.get_rect(center=[560,360])
        screen.blit(skillbutton_image, skillbutton_rect)
        
        skill_button = {
                  '(1)Attack: 0 MP':(560,360),\
                  '(2)Light: 10 MP':(560,400),\
                  '(3)Heal:  30 MP':(560,440)}
        
        for my_text, text_pos in skill_button.items():
            text_surface = my_font.render(my_text, True, white)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)

        mon_rect = mon_rect.move(speed)
        
        mon_info = 'lv: '+str(Monster.lv)+'  '+Monster.name
        info_button = {mon_info:((mon_rect.right+mon_rect.left)/2,\
                                   mon_rect.top-20)}
        
        if mon_rect.left < 220 or mon_rect.right > width-220:
            speed[0] = -speed[0]
        if mon_rect.top < 130 or mon_rect.bottom > height-130:
            speed[1] = -speed[1]
        
        # add the rectangle containing the monster to this screen
        screen.blit(mon_image, mon_rect)
        
        # show monster's hp with rect
        pygame.draw.rect(screen,green,((mon_rect.right+mon_rect.left)/2-Monster.hp/2,\
                                       mon_rect.top-10,\
                                       Monster.hp,
                                       10),0)
        
        
        # add the info of monster to this screen
        for my_text, text_pos in info_button.items():
            text_surface = my_font.render(my_text, True, white)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
            
        attack = check_attack(mon_rect)
        #if check_attack() == 1:
            #Monster.hp = 0
        if attack == 1:
            Monster.hp -= player.atk

            atk_rect = atk_image.get_rect(center=[int(uniform(mon_rect.left,\
                                                              mon_rect.right)),\
                                                  int(uniform(mon_rect.top,\
                                                              mon_rect.bottom))])
            screen.blit(atk_image, atk_rect)
            #print("Monster's remaining HP: "+str(Monster.hp))

        elif attack == 2:
            #print("Lighting")
            if player.mp >= 10:
                Monster.hp -= player.atk * 1.5
                player.mp -=10
                
                screen.blit(skill_image, skill_rect)
                
        elif attack == 3:
            #print("Heal")
            if player.mp >= 30:
                player.mp -= 30
                
                player.hp += 50
                if player.hp > 100:
                    player.hp = 100
                
                heal_rect = heal_image.get_rect(center=[int(uniform(hero_rect.left,\
                                                              hero_rect.right)),\
                                                  int(uniform(hero_rect.top,\
                                                              hero_rect.bottom))])
                screen.blit(heal_image, heal_rect)
 
        pygame.display.flip()
        
    if Monster.hp <= 0:
        Monster.hp = full_hp
        Monster.lv += 1
        Monster.hp += (Monster.mid-1)*4
    
    
        player.exp += Monster.exp
        if player.exp >= 100:
            player.lv += 1
            player.hp = 100
            player.mp = 100
            player.atk += 2
            player.exp -= 100
            
    else:
        Monster.hp = full_hp
        screen.blit(dead_image, dead_rect)

    pygame.mixer.music.stop()
    
# using pygame event to check if you are attacking
def check_attack(rect):
    global flag,display_mode
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            
            if y > 360-15 and y < 360+15:
                if x > 560-50 and x < 560+50:
                    return 1
            
            if y > 400-15 and y < 400+15:
                if x > 560-50 and x < 560+50:
                    return 2
                    
            if y > 440-15 and y < 440+15:
                if x > 560-50 and x < 560+50:
                    return 3

            if y > rect.top and y < rect.bottom:
                if x > rect.left and x < rect.right:
                    return 1

            if y > 0 and y < 20:
                if x > 620 and x < 640:
                    flag = False

            if y > map_rect.top and y < map_rect.bottom:
                if x > map_rect.left and x < map_rect.right:
                    display_mode = not display_mode


	elif event.type == pygame.KEYDOWN:
	    if event.key == pygame.K_1:
		return 1
	    elif event.key == pygame.K_2:
		return 2
	    elif event.key == pygame.K_3:
		return 3

    return 0

#################################### Moving #########################################

# using pygame event to check your commands for moving
def check_direction():
    global flag,display_mode
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            
            if y > forward_rect.top and y < forward_rect.bottom:
                if x > forward_rect.left and x < forward_rect.right:
                    Forward()
            
            if y > backward_rect.top and y < backward_rect.bottom:
                if x > backward_rect.left and x < backward_rect.right:
                    Backward()
                    
            if y > right_rect.top and y < right_rect.bottom:
                if x > right_rect.left and x < right_rect.right:
                    Right()
                    
            if y > left_rect.top and y < left_rect.bottom:
                if x > left_rect.left and x < left_rect.right:
                    Left()

            if y > 0 and y < 20:
                if x > 620 and x < 640:
                    flag = False

            if y > map_rect.top and y < map_rect.bottom:
                if x > map_rect.left and x < map_rect.right:
                    display_mode = not display_mode
	  

	elif event.type == pygame.KEYDOWN:
	    if event.key == pygame.K_w:
		Forward()
	    elif event.key == pygame.K_s:
		Backward()
	    elif event.key == pygame.K_a:
		Left()
	    elif event.key == pygame.K_d:
		Right()
            elif event.key == pygame.K_q:
                sLeft()
            elif event.key == pygame.K_e:
                sRight()

def Forward():
    global pos,move,move_start
    if pos[2] == 1:
        for i in range(5):
	    for j in range(4):
	    	map[i+1][j+1] = map[i+1][j+2]
	    map[i+1][5] = 1
	rand = int(uniform(1.0,9.0))
	if rand <= 8:
	    map[int(uniform(1.0,6.0))][5] = rand
    elif pos[2] == 2:
        for i in range(5):
	    for j in range(4):
	    	map[5-j][i+1] = map[4-j][i+1]
	    map[1][i+1] = 1
	rand = int(uniform(1.0,9.0))
	if rand <= 8:
	    map[1][int(uniform(1.0,6.0))] = rand
    elif pos[2] == 3:
        for i in range(5):
	    for j in range(4):
	    	map[i+1][5-j] = map[i+1][4-j]
	    map[i+1][1] = 1
	rand = int(uniform(1.0,9.0))
	if rand <= 8:
	    map[int(uniform(1.0,6.0))][1] = rand
    elif pos[2] == 4:
        for i in range(5):
	    for j in range(4):
	    	map[j+1][i+1] = map[j+2][i+1]
	    map[5][i+1] = 1
	rand = int(uniform(1.0,9.0))
	if rand <= 8:
	    map[5][int(uniform(1.0,6.0))] = rand
        
    set_direction(1,-1)
    set_direction(2,1)
    move = 1
    move_start = time.time()  

def Backward():
    global pos,move,move_start
    if pos[2] == 1:
        for i in range(5):
	    for j in range(4):
	    	map[i+1][5-j] = map[i+1][4-j]
	    map[i+1][1] = 1
	rand = int(uniform(1.0,9.0))
	if rand <= 8:
	    map[int(uniform(1.0,6.0))][1] = rand
    elif pos[2] == 2:
        for i in range(5):
	    for j in range(4):
	    	map[j+1][i+1] = map[j+2][i+1]
	    map[5][i+1] = 1
	rand = int(uniform(1.0,9.0))
	if rand <= 8:
	    map[5][int(uniform(1.0,6.0))] = rand
    elif pos[2] == 3:
        for i in range(5):
	    for j in range(4):
	    	map[i+1][j+1] = map[i+1][j+2]
	    map[i+1][5] = 1
	rand = int(uniform(1.0,9.0))
	if rand <= 8:
	    map[int(uniform(1.0,6.0))][5] = rand
    elif pos[2] == 4:
        for i in range(5):
	    for j in range(4):
	    	map[5-j][i+1] = map[4-j][i+1]
	    map[1][i+1] = 1
	rand = int(uniform(1.0,9.0))
	if rand <= 8:
	    map[1][int(uniform(1.0,6.0))] = rand

    set_direction(1,1)
    set_direction(2,-1)
    move = 1
    move_start = time.time()

def Right():
    global pos,move,move_start
    if pos[2] == 1:
        pos[2] = 4
    else:
        pos[2] -= 1

    set_direction(1,1)
    set_direction(2,1)
    move = 2
    move_start = time.time()

def Left():
    global pos,move,move_start
    if pos[2] == 4:
        pos[2] = 1
    else:
        pos[2] += 1
    set_direction(2,-1)
    set_direction(1,-1)
    move = 2
    move_start = time.time()

# make a small right turn
def sRight():
    global move,move_start
    set_direction(1,1)
    set_direction(2,1)
    
    time.sleep(0.1)
    set_direction(1,0)
    set_direction(2,0)

# make a small left turn
def sLeft():
    global move,move_start
    set_direction(2,-1)
    set_direction(1,-1)
    
    time.sleep(0.1)
    set_direction(1,0)
    set_direction(2,0)

############################## generate title page ################################

def check_click():
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
	    return 1

    return 0

pygame.mixer.music.load('Netherplace.ogg')
pygame.mixer.music.play(-1)
 
mon_list = np.array([1,2,3,4,5,1,2])
mon_pos = np.array([[0,480-25],[-120,480-25],[-240,480-25],[-360,480-25],\
	   [-480,480-25],[-600,480-25],[-720,480-25]])
mon_spd = np.array([[1,-uniform(1.0,15.0)],[1,-uniform(1.0,15.0)],\
	[1,-uniform(1.0,15.0)],[1,-uniform(1.0,15.0)],\
	[1,-uniform(1.0,15.0)],[1,-uniform(1.0,15.0)],\
	[1,-uniform(1.0,15.0)]])

while True:
    # fill the screen with black
    screen.fill(black)

    screen.blit(pi_image,pi_rect)
    screen.blit(ar_image,ar_rect)
    screen.blit(game_image,game_rect)

    if check_click():
	break

    for i in range(len(mon_list)):
	if mon_list[i] == 1:
	    mon_img = pygame.image.load(bat.pic)
	elif mon_list[i] == 2:
	    mon_img = pygame.image.load(centaur.pic)
	elif mon_list[i] == 3:
	    mon_img = pygame.image.load(angryboy.pic)
	elif mon_list[i] == 4:
	    mon_img = pygame.image.load(pumpkin.pic)
	elif mon_list[i] == 5:
	    mon_img = pygame.image.load(dragon.pic)

	#mon_img = pygame.image.load(mon_list[i].pic)
        mon_rect = mon_img.get_rect(center=(mon_pos[i][0],mon_pos[i][1]))

	# make monster jump
	if mon_rect.bottom > 480:
	    mon_spd[i][1] = -uniform(1.0,15.0)

	mon_rect = mon_rect.move(mon_spd[i])
	mon_spd[i][1] += 0.5

        screen.blit(mon_img,mon_rect)

	mon_pos[i][0] = mon_rect.center[0]
	mon_pos[i][1] = mon_rect.center[1]

    if mon_pos[0][0]-25 > 640:
	for i in range(len(mon_list)-1):
	    mon_list[i] = mon_list[i+1]
	    mon_pos[i] = mon_pos[i+1]
	    mon_spd[i] = mon_spd[i+1]
	ran_mon = int(uniform(1.0,6.0))
	if ran_mon == 1:
	    mon_list[len(mon_list)-1] = 1
	elif ran_mon == 2:
	    mon_list[len(mon_list)-1] = 2
	elif ran_mon == 3:
	    mon_list[len(mon_list)-1] = 3
	elif ran_mon == 4:
	    mon_list[len(mon_list)-1] = 4
	elif ran_mon == 5:
	    mon_list[len(mon_list)-1] = 5
	mon_pos[len(mon_list)-1][0] = mon_pos[len(mon_list)-2][0]-120
	mon_pos[len(mon_list)-1][1] = 480-25
	mon_spd[len(mon_list)-1][0] = 1
	mon_spd[len(mon_list)-1][1] = -uniform(1.0,15.0)

    # display the whole screen
    pygame.display.flip()
    time.sleep(0.03)

############################## input name page #####################################

NM_Font = pygame.font.Font(None,50)
done = False
name = ''
input_box = pygame.Rect(240,300,160,50)

Button_Enter = 'ENTER'
Enter_Font = pygame.font.Font(None,40)
Enter_surface = Enter_Font.render(Button_Enter,True,white)
Enter_box = pygame.Rect(500,430,100,40)

Text1 = 'Hi Player:'
Text2 = 'Write down your name and start a great adventure.'
Text_Font = pygame.font.Font(None,30)
Text1_surface = Text_Font.render(Text1,True,white)
Text2_surface = Text_Font.render(Text2,True,white)

while not done:
    for event in pygame.event.get():
	if event.type == pygame.KEYDOWN:
	    if event.key == pygame.K_BACKSPACE:
		name = name[:-1]
	    elif event.key == pygame.K_RETURN:
		done = True
	    else:
		if len(name) <= 7:
		    name += event.unicode
        elif(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos

            if x > 500 and x < 600:
            	if y > 430 and y < 470:
                    done = True

    # fill the screen with black
    screen.fill(black)

    screen.blit(Text1_surface,(50,50))
    screen.blit(Text2_surface,(80,80))

    name_surface = NM_Font.render(name,True,white)
    screen.blit(name_surface,(245,305))
    pygame.draw.rect(screen,white,input_box,2)

    screen.blit(Enter_surface,(505,435))
    pygame.draw.rect(screen,white,Enter_box,2)

    pygame.display.flip()
    time.sleep(0.01)

pygame.mixer.music.stop()

################################ main game ####################################

# Save the position and orientation of player
# ori:
# 1 -- facing right
# 2 -- facing up
# 3 -- facing left
# 4 -- facing down
pos = np.array([3,3,1])

# initialize map
map = map_generator()

move = 0
move_start = 0

# flag is the global value controling the running of pygame
# it's default value is True
flag = True

# use flag to control the running, if flag value is False, end the loop
while flag:
    facing = check_facing(pos,map)
       
    # generate the background
    background()
    
    if move == 0:
    	if map[pos[0],pos[1]] == 1:
            # generate monsters
            generate_monster(facing[0],[100,240])
            generate_monster(facing[1],[320,200])
            generate_monster(facing[2],[540,240])
    	elif map[pos[0],pos[1]] == 2:
            encountering_monster(bat)
            map[pos[0],pos[1]] = 1
    	elif map[pos[0],pos[1]] == 3:
            encountering_monster(centaur)
            map[pos[0],pos[1]] = 1
    	elif map[pos[0],pos[1]] == 4:
            encountering_monster(angryboy)
            map[pos[0],pos[1]] = 1
    	elif map[pos[0],pos[1]] == 5:
            encountering_monster(pumpkin)
            map[pos[0],pos[1]] = 1
    	elif map[pos[0],pos[1]] == 6:
            encountering_monster(dragon)
            map[pos[0],pos[1]] = 1
	elif map[pos[0],pos[1]] == 7:
	    player.atk += 10
	    map[pos[0],pos[1]] = 1
	elif map[pos[0],pos[1]] == 8:
	    player.hp = 100
	    player.mp = 100
	    map[pos[0],pos[1]] = 1

    	draw_movebutton()
    	check_direction()

    elif move == 1:
	if time.time()-move_start > 1:
    	    set_direction(1,0)
    	    set_direction(2,0)
	    move = 0
    elif move == 2:
	if time.time()-move_start > 0.5:
    	    set_direction(1,0)
    	    set_direction(2,0)
	    move = 0	    
    
    # display the whole screen
    pygame.display.flip()
    time.sleep(0.01)

################################## END PAGE ##################################

pygame.mixer.music.load('Netherplace.ogg')
pygame.mixer.music.play(-1)

Text1 = 'Thank You For Playing!'
Text2 = 'Made By:'
Text3 = 'Mengde Wu'
Text4 = 'Yexiang Chang'
Text_Font = pygame.font.Font(None,30)
Text1_surface = Text_Font.render(Text1,True,white)
Text2_surface = Text_Font.render(Text2,True,white)
Text3_surface = Text_Font.render(Text3,True,white)
Text4_surface = Text_Font.render(Text4,True,white)

mon_list = np.array([1,2,3,4,5,1,2])
mon_pos = np.array([[0,480-25],[-120,480-25],[-240,480-25],[-360,480-25],\
	   [-480,480-25],[-600,480-25],[-720,480-25]])
mon_spd = np.array([[1,-uniform(1.0,15.0)],[1,-uniform(1.0,15.0)],\
	[1,-uniform(1.0,15.0)],[1,-uniform(1.0,15.0)],\
	[1,-uniform(1.0,15.0)],[1,-uniform(1.0,15.0)],\
	[1,-uniform(1.0,15.0)]])

while True:
    # fill the screen with black
    screen.fill(black)

    screen.blit(Text1_surface,(80,60))
    screen.blit(Text2_surface,(400,80))
    screen.blit(Text3_surface,(410,100))
    screen.blit(Text4_surface,(410,120))

    if check_click():
	break

    for i in range(len(mon_list)):
	if mon_list[i] == 1:
	    mon_img = pygame.image.load(bat.pic)
	elif mon_list[i] == 2:
	    mon_img = pygame.image.load(centaur.pic)
	elif mon_list[i] == 3:
	    mon_img = pygame.image.load(angryboy.pic)
	elif mon_list[i] == 4:
	    mon_img = pygame.image.load(pumpkin.pic)
	elif mon_list[i] == 5:
	    mon_img = pygame.image.load(dragon.pic)

	#mon_img = pygame.image.load(mon_list[i].pic)
        mon_rect = mon_img.get_rect(center=(mon_pos[i][0],mon_pos[i][1]))

	# make monster jump
	if mon_rect.bottom > 480:
	    mon_spd[i][1] = -uniform(1.0,15.0)

	mon_rect = mon_rect.move(mon_spd[i])
	mon_spd[i][1] += 0.5

        screen.blit(mon_img,mon_rect)

	mon_pos[i][0] = mon_rect.center[0]
	mon_pos[i][1] = mon_rect.center[1]

    if mon_pos[0][0]-25 > 640:
	for i in range(len(mon_list)-1):
	    mon_list[i] = mon_list[i+1]
	    mon_pos[i] = mon_pos[i+1]
	    mon_spd[i] = mon_spd[i+1]
	ran_mon = int(uniform(1.0,6.0))
	if ran_mon == 1:
	    mon_list[len(mon_list)-1] = 1
	elif ran_mon == 2:
	    mon_list[len(mon_list)-1] = 2
	elif ran_mon == 3:
	    mon_list[len(mon_list)-1] = 3
	elif ran_mon == 4:
	    mon_list[len(mon_list)-1] = 4
	elif ran_mon == 5:
	    mon_list[len(mon_list)-1] = 5
	mon_pos[len(mon_list)-1][0] = mon_pos[len(mon_list)-2][0]-120
	mon_pos[len(mon_list)-1][1] = 480-25
	mon_spd[len(mon_list)-1][0] = 1
	mon_spd[len(mon_list)-1][1] = -uniform(1.0,15.0)

    # display the whole screen
    pygame.display.flip()
    time.sleep(0.03)

pygame.mixer.music.stop()

############################ Clean Up ##################################

s1.stop()
s2.stop()
GPIO.cleanup()
pygame.quit()
cv2.destroyAllWindows()
