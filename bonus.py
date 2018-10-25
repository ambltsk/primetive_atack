# -*- coding: utf-8 -*-

import pygame as pg

class Bonus(pg.sprite.Sprite):
	
	def __init__(self, type_bonus, life):
		pg.sprite.Sprite.__init__(self)
