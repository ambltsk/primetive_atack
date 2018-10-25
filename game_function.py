# -*- coding: utf-8 -*-

import sys
from math import *
import pygame as pg
from config import *
from bullet import Bullet

def side(point_b, point_st):
	side_h = ""
	side_v = ""
	if point_b[0] < point_st[0]:
		side_h = 'left'
	elif point_b[0] > point_st[0]:
		side_h = 'right'
	else:
		side_h = 'center'
	if point_b[1] < point_st[1]:
		side_v = 'top'
	elif point_b[1] > point_st[1]:
		side_v = 'bottom'
	else:
		side_v = 'center'
	if fabs(point_b[0] - point_st[0]) >= fabs(point_b[1] - point_st[1]):
		return side_h
	else:
		return side_v

def collision(bullets, enemys, sound):
	bullet_out(bullets)
	bullet_hit_enemy(bullets, enemys, sound)
	enemy_out(enemys)
	

def bullet_out(bullets):
	#Уничтожение пуль ушедших за край экрана
	for bullet in bullets:
		if bullet.position[0] < 0 or bullet.position[0] > WIDTH:
			bullets.remove(bullet)
		if bullet.position[1] < 0 or bullet.position[1] > HEIGHT:
			bullets.remove(bullet)

def enemy_out(enemys):
	#Удаление убитых врагов
	for enemy in enemys:
		if enemy.deadth:
			enemys.remove(enemy)

def bullet_hit_enemy(bullets, enemys, sound):
	#проверка пападания пуль во врагов
	for enemy in enemys:
		for bullet in bullets:
			if not enemy.killed:
				if enemy.rect.colliderect(bullet.rect):
					if not bullet.is_hit_this_enemy(enemy):
						enemy.hit_me()
						if not cnfg.mute:
							sound.play()
						if bullet.bullet_type == BULLET_THROUGH:
							bullet.enemy_add(enemy)
						cnfg.game_score += 1
					if bullet.bullet_type == BULLET_ABSORPTION:
						bullets.remove(bullet)
					elif bullet.bullet_type == BULLET_MIRROR:
						s = side(bullet.rect.center, enemy.rect.center)
						bullet.mirror(s)


def bullet_add(main_sc, main_hero, bullets):
	if cnfg.is_blt_fun:
		#если есть бонус веером по 5 пуль под угломи 5 градусов
		angel = main_hero.angel
		angel -= 10
		for i in range(0, 5):
			bullet = Bullet(main_sc,angel)
			bullets.add(bullet)
			angel += 5
	else:
		#без бонуса по одной
		bullet = Bullet(main_sc, main_hero.angel)
		bullets.add(bullet)
