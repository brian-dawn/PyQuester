
import random

def add_building(level, x_coord, y_coord, x_size=5, y_size=5):
	## Add the left wall
	for j in xrange(y_coord, y_coord + y_size):
		level.set_tile(x_coord, j, 'stone_wall')
		#level._tiles[x_coord][j].is_under_sky = False
		#level._tiles[x_coord][j]._set_texture(media.get_texture('tile'))
	
	for i in xrange(x_coord + 1, x_coord + x_size - 1):
		## Add the top wall
		level.set_tile(i, y_coord, 'stone_wall')
		#level._tiles[i][y_coord].is_under_sky = False
		#level._tiles[i][y_coord]._set_texture(media.get_texture('tile'))
		
		## Add the interior texture
		for j in xrange(y_coord + 1, y_coord + y_size - 1):
			level.set_tile(i, j, 'wood_floor')
		#	level._tiles[i][j].is_under_sky = False
		#	level._tiles[i][j]._set_texture(media.get_texture('wood'))
		
		## Add the bottom wall
		level.set_tile(i, y_coord + y_size - 1, 'stone_wall')
		#level._tiles[i][y_coord + y_size - 1].is_under_sky = False
		#level._tiles[i][y_coord + y_size - 1]._set_texture(media.get_texture('tile'))
	
	## Add the right wall
	for j in xrange(y_coord, y_coord + y_size):
		level.set_tile(x_coord + x_size - 1, j, 'stone_wall')
		#level._tiles[x_coord + x_size - 1][j].is_under_sky = False
		#level._tiles[x_coord + x_size - 1][j]._set_texture(media.get_texture('tile'))
	
	## Add a door to the building, randomly located along the walls
	## In the future, possibly vary the number of doors?
	rand = random.uniform(0,4)
	print "rand =", rand
	side_with_door = int(rand)
	print "Side with door:", side_with_door
	if ( side_with_door == 1 ):
		door_position = int((x_size - 2)*random.random())
		print "Door position:", door_position
		door_coord = x_coord + door_position + 1
		
		# For some reason, when these level.set_tile() lines are uncommented
		# segfaults happen and the game crashes.  Not sure why
		#level.set_tile(x_coord + door_position + 1, y_coord, 'wood_floor')
		
		# Old version of the code
		#level._tiles[door_coord][y_coord].is_under_sky = False
		#level._tiles[door_coord][y_coord]._set_texture(media.get_texture('wood'))
	elif ( side_with_door == 2 ):
		door_position = int((y_size - 2)*random.random())
		print "Door position:", door_position
		door_coord = y_coord + door_position + 1
		#level.set_tile(x_coord, y_coord + door_position + 1, 'wood_floor')
		#level._tiles[x_coord][door_coord].is_under_sky = False
		#level._tiles[x_coord][door_coord]._set_texture(media.get_texture('wood'))
	elif ( side_with_door == 3 ):
		door_position = int((x_size - 2)*random.random())
		print "Door position:", door_position
		door_coord = x_coord + door_position + 1
		#level.set_tile(x_coord + door_position + 1, y_coord + y_size, 'wood_floor')
		#level._tiles[door_coord][y_coord + y_size].is_under_sky = False
		#level._tiles[door_coord][y_coord + y_size]._set_texture(media.get_texture('wood'))
	else:
		door_position = int((y_size - 2)*random.random())
		print "Door position:", door_position
		door_coord = y_coord + door_position + 1
		#level.set_tile(x_coord + x_size, y_coord + door_position + 1, 'wood_floor')
		#level._tiles[x_coord + x_size][door_coord].is_under_sky = False
		#level._tiles[x_coord + x_size][door_coord]._set_texture(media.get_texture('wood'))
		


import media
