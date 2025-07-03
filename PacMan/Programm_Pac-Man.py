Class Wall:
	def __init__(self, locationy, locationx)
			self.locationy 	= int(locationy)
			self.locationx 	= int(locationx)

Class Point:
	def __init__(self, locationy, locationx, valueP)
			self.locationy 	= int(locationy)
			self.locationx 	= int(locationx)
			self.valueP 	= int(valueP)
	def increasescore(self, score):
			return score = score + self.valueP  #score = Point.increasescore

	def remove(self):
			self.locationx = 0
			self.locationy = 0

Class Ghost:
	def __init__(self, starty, startx, valueG, color, name)
			self.locationy	= int(starty)
			self.locationx	= int(startx)
			self.valueG		= int(valueG)
			self.color		= color
			self.name		= name
			self.starty		= int(starty)
			self.startx		= int(startx)

	def increasescore(self, score):
			return score = score + self.valueG

	#def move(self)


	def die(self, score)											#score = Point.increasescore
			self.locationy = self.starty
			self.locationx = self.startx
			return self.increasescore
		
Class Player:
	def __init__(self)
		self.startPy		= 9
		self.startPx 		= 7
		self.name 			= PacMan
		self.color 			= (255,215,0)
		self.pill			=int(0)
		self.health			= int(3)
	
	#def checkghost(self)

	def checkwall





while True:
	wallsY = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6,7,7,7,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,13,13,13,13,14,14,15,15,15,15,15,15,15,15,15,15,15,15,15,15]
	wallsX = [0,1,2,3,4,5,6,9,10,11,12,13,14,15,0,15,0,2,3,4,5,7,8,9,11,12,13,15,0,7,9,11,13,15,0,3,5,7,8,9,11,13,15,0,1,3,11,13,15,0,1,3,5,6,8,9,11,12,13,15]