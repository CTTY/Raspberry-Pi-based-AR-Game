#!/usr/bin/env python
# Team member: name: Mengde Wu netId: mw934
#              name: Yexiang Chang netId: yc2523
import numpy as np
from random import uniform
import pygame
from pygame.locals import *
import sys, termios, tty, os
import time
import RPi.GPIO as GPIO
import cv2
import subprocess


# setup the callback routine, the system will run the callback function
# if it detects a falling edge in one of these GPIOs
GPIO.setmode(GPIO.BCM) 
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

s1 = GPIO.PWM(26, 46.5)
s2 = GPIO.PWM(5, 46.5)
s1.start(0)
s2.start(0)


# num:1 left servo
#     2 right servo

# dir:1 clockwise
#     -1 counterclockwise
#     0 stop
def set_direction(num,dir):
    if num==1:
        if dir==1:
            dc=7.8
        elif dir==0:
            dc=0
        elif dir==-1:
            dc=6.0
        s1.ChangeDutyCycle(dc)
    elif num==2:
        if dir==1:
            dc=7.8
        elif dir==0:
            dc=0
        elif dir==-1:
            dc=6.0
        s2.ChangeDutyCycle(dc)

class Monster:
    def __init__(self,Skill,mid,pic,lv,name,hp,atk,defen,money,exp):
        self.Skill=Skill
        self.mid = mid
        self.pic = pic
        self.lv = lv
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defen = defen
        self.money = money
        self.exp = exp
    
class Skill:
    def __init__(self,name,dmg,pic,cost):
        self.name = name
        self.dmg = dmg
        self.pic = pic
        self.cost = cost   
        
class Player:
    def __init__(self,Skill,hp,mp,lv,exp,atk,death):
        self.Skill = Skill
        self.hp = hp
        self.mp = mp
        self.lv = lv
        self.exp = exp
        self.atk = atk
        self.death = death

def map_generator():

    map = np.zeros(49).reshape(7,7)

    for i in range(5):
        for j in range(5):
            map[i+1,j+1] = int(uniform(1.0,21.0))
            if map[i+1,j+1] >= 7:
                map[i+1,j+1] = 1
                
    map[3,3] = 1
    return map

def check_facing(pos,map):
    if pos[2] == 1:
        facing = np.array([int(map[pos[0]-1,pos[1]+1]),\
                           int(map[pos[0],pos[1]+1]),\
                           int(map[pos[0]+1,pos[1]+1])])
    elif pos[2] == 2:
        facing = np.array([int(map[pos[0]-1,pos[1]-1]),\
                           int(map[pos[0]-1,pos[1]]),\
                           int(map[pos[0]-1,pos[1]+1])])
    elif pos[2] == 3:
        facing = np.array([int(map[pos[0]+1,pos[1]-1]),\
                           int(map[pos[0],pos[1]-1]),\
                           int(map[pos[0]-1,pos[1]-1])])
    elif pos[2] == 4:
        facing = np.array([int(map[pos[0]+1,pos[1]+1]),\
                           int(map[pos[0]+1,pos[1]]),\
                           int(map[pos[0]+1,pos[1]-1])])
    
    return facing

# check if all the monsters in the map are killed
def check_map(map):
    if np.max(map) == 1:
	return 1
    return 0

# initialize monsters
rush = Skill(name='rush',dmg=1,pic='',cost=1)
bat = Monster(rush,mid=1,pic='bat.png',lv=1,name='Bat',\
                 hp=4,atk=1,defen=1,money=1,exp=5)
centaur = Monster(rush,mid=2,pic='centaur.png',lv=1,name='Centaur',\
                 hp=8,atk=5,defen=5,money=10,exp=10)
angryboy = Monster(rush,mid=3,pic='angryboy.png',lv=1,name='Angryboy',\
                 hp=16,atk=10,defen=8,money=100,exp=15)
pumpkin = Monster(rush,mid=4,pic='pumpkin.png',lv=1,name='Pumpkin',\
                 hp=32,atk=15,defen=15,money=500,exp=30)
dragon = Monster(rush,mid=5,pic='dragon.png',lv=1,name='Dragon',\
                 hp=64,atk=20,defen=30,money=1000,exp=50)

# initialize player
player = Player(rush,hp=100,mp=100,lv=1,exp=0,atk=8,death=0)
