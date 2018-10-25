# -*- coding: utf-8 -*-

import pygame as pg
from config import *
from math import *

def calc_dspeed(angel, speed):
	dx = -speed * cos((angel-90)*pi/180)
	dy = speed * sin((angel-90)*pi/180)
	return [dx, dy]

class Bullet(pg.sprite.Sprite):
	"""Класс реализующий пули"""
	def __init__(self, main_sc, angel):
		pg.sprite.Sprite.__init__(self)
		self.sc = main_sc
		self.position = [WIDTH // 2, HEIGHT // 2]
		self.angel = angel
		self.speed = cnfg.blt_speed
		self.dspeed = calc_dspeed(self.angel, self.speed)
		self.color = BULLET_COLOR[2]
		self.contur_color = BULLET_CONTUR_COLOR[2]
		self.bullet_type = cnfg.blt_type
		self.hit_enemy = []
		if self.bullet_type == BULLET_ABSORPTION:
			self.color = BULLET_COLOR[0]
			self.contur_color = BULLET_CONTUR_COLOR[0]
		elif self.bullet_type == BULLET_THROUGH:
			self.color = BULLET_COLOR[1]
			self.contur_color = BULLET_CONTUR_COLOR[1]
		else:
			self.color = BULLET_COLOR[2]
			self.contur_color = BULLET_CONTUR_COLOR[2]
		self.radius = cnfg.blt_size
		self.rect = pg.rect.Rect((self.position[0] - self.radius,
								self.position[1] - self.radius),
								(2 * self.radius,
								 2 * self.radius))
	
	def blitme(self):
		pg.draw.circle(self.sc,
						self.color,
						(int(self.position[0]), int(self.position[1])),
						self.radius)
		pg.draw.circle(self.sc,
						self.contur_color,
						(int(self.position[0]), int(self.position[1])),
						self.radius, 2)
	
	def update(self):
		self.position[0] += self.dspeed[0]
		self.position[1] += self.dspeed[1]
		self.rect.center = self.position
	
	def enemy_add(self, enemy):
		self.hit_enemy.append(enemy)
	
	def is_hit_this_enemy(self, enemy):
		if len(self.hit_enemy) == 0:
			return False
		else:
			flag = False
			for e in self.hit_enemy:
				if e == enemy:
					flag = True
			return flag
	
	def mirror(self, side):
		if side == 'left' or side == 'right':
			self.dspeed[0] *= -1
		if side == 'top' or side == 'bottom':
			self.dspeed[1] *= -1
