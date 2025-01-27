import math

from statemachine import StateMachine, State

import gng.global_constants as gc

class ManualControls(StateMachine):
	stationary = State(initial=True)
	up         = State()
	down       = State()
	left       = State()
	right      = State()
	upleft     = State()
	upright    = State()
	downleft   = State()
	downright  = State()

	press_up = (
		stationary.to(up) |
		up.to(up) |
		down.to(up) |
		left.to(upleft) |
		right.to(upright) |
		upleft.to(upleft) |
		upright.to(upright) |
		downleft.to(upleft) |
		downright.to(upright)
	)
	press_down = (
		stationary.to(down) |
		up.to(down) |
		down.to(down) |
		left.to(downleft) |
		right.to(downright) |
		upleft.to(downleft) |
		upright.to(downright) |
		downleft.to(downleft) |
		downright.to(downright)
	)
	press_left = (
		stationary.to(left) |
		up.to(upleft) |
		down.to(downleft) |
		left.to(left) |
		right.to(left) |
		upleft.to(upleft) |
		upright.to(upleft) |
		downleft.to(downleft) |
		downright.to(downleft)
	)
	press_right = (
		stationary.to(right) |
		up.to(upright) |
		down.to(downright) |
		left.to(right) |
		right.to(right) |
		upleft.to(upright) |
		upright.to(upright) |
		downleft.to(downright) |
		downright.to(downright)
	)
	release_up = (
		stationary.to(stationary) |
		up.to(stationary) |
		down.to(down) |
		left.to(left) |
		right.to(right) |
		upleft.to(left) |
		upright.to(right) |
		downleft.to(downleft) |
		downright.to(downright)
	)
	release_down = (
		stationary.to(stationary) |
		up.to(up) |
		down.to(stationary) |
		left.to(left) |
		right.to(right) |
		upleft.to(upleft) |
		upright.to(upright) |
		downleft.to(left) |
		downright.to(right)
	)
	release_left = (
		stationary.to(stationary) |
		up.to(up) |
		down.to(down) |
		left.to(stationary) |
		right.to(right) |
		upleft.to(up) |
		upright.to(upright) |
		downleft.to(down) |
		downright.to(downright)
	)
	release_right = (
		stationary.to(stationary) |
		up.to(up) |
		down.to(down) |
		left.to(left) |
		right.to(stationary) |
		upleft.to(upleft) |
		upright.to(up) |
		downleft.to(downleft) |
		downright.to(down)
	)
	to_stationary = (
		stationary.to(stationary) |
		up.to(stationary) |
		down.to(stationary) |
		left.to(stationary) |
		right.to(stationary) |
		upleft.to(stationary) |
		upright.to(stationary) |
		downleft.to(stationary) |
		downright.to(stationary)
	)
	obstruction_up = (
		stationary.to(stationary) |
		up.to(stationary) |
		down.to(down) |
		left.to(left) |
		right.to(right) |
		upleft.to(left) |
		upright.to(right) |
		downleft.to(downleft) |
		downright.to(downright)
	)
	obstruction_down = (
		stationary.to(stationary) |
		up.to(up) |
		down.to(stationary) |
		left.to(left) |
		right.to(right) |
		upleft.to(upleft) |
		upright.to(upright) |
		downleft.to(left) |
		downright.to(right)
	)
	obstruction_left = (
		stationary.to(stationary) |
		up.to(up) |
		down.to(down) |
		left.to(stationary) |
		right.to(right) |
		upleft.to(up) |
		upright.to(upright) |
		downleft.to(down) |
		downright.to(downright)
	)
	obstruction_right = (
		stationary.to(stationary) |
		up.to(up) |
		down.to(down) |
		left.to(left) |
		right.to(stationary) |
		upleft.to(upleft) |
		upright.to(up) |
		downleft.to(downleft) |
		downright.to(down)
	)


	# ------------------------------------------------------------------
	# ------------------------------------------------------------------
	# ------------------------------------------------------------------

	def __init__(
		self, 
		puppet, 
		list_of_entities,
		list_of_npcs,
		list_of_items_on_ground,
		list_of_collision_rects, 
	):
		self.puppet                           = puppet
		self.list_of_entities                 = list_of_entities
		self.list_of_npcs                     = list_of_npcs
		self.list_of_items_on_ground          = list_of_items_on_ground
		self.list_of_collision_rects          = list_of_collision_rects
		self.current_frame_obstruction_up     = None
		self.current_frame_obstruction_down   = None
		self.current_frame_obstruction_left   = None
		self.current_frame_obstruction_right  = None
		self.previous_frame_obstruction_up    = None
		self.previous_frame_obstruction_down  = None
		self.previous_frame_obstruction_left  = None
		self.previous_frame_obstruction_right = None
		self.current_direction_facing         = None
		super().__init__()

	def next_coordinates(self, direction):
		match direction:
			case self.stationary: 
				return (
					self.puppet.x, 
					self.puppet.y
				)
			case self.up:
				return (
					self.puppet.x, 
					self.puppet.y - self.puppet.speed
				)
			case self.down:
				return (
					self.puppet.x,
					self.puppet.y + self.puppet.speed
				)
			case self.left:
				return (
					self.puppet.x - self.puppet.speed,
					self.puppet.y
				)
			case self.right:
				return (
					self.puppet.x + self.puppet.speed,
					self.puppet.y
				)
			case self.upleft:
				return (
					self.puppet.x - self.puppet.speed/math.sqrt(2),
					self.puppet.y - self.puppet.speed/math.sqrt(2)
				)
			case self.upright:
				return (
					self.puppet.x + self.puppet.speed/math.sqrt(2),
					self.puppet.y - self.puppet.speed/math.sqrt(2)
				)
			case self.downleft:
				return (
					self.puppet.x - self.puppet.speed/math.sqrt(2),
					self.puppet.y + self.puppet.speed/math.sqrt(2)
				)
			case self.downright:
				return (
					self.puppet.x + self.puppet.speed/math.sqrt(2),
					self.puppet.y + self.puppet.speed/math.sqrt(2)
				)
			case _:
				print(
					f"An unexpected value {direction} was plugged into "\
					"the next_direction() method in player_functions.py."
				)

	def next_wall(self, direction):
		(next_x, next_y) = self.next_coordinates(direction)
		next_rect = gc.pygame.Rect(
			next_x, next_y, 
			self.puppet.height, self.puppet.width
		)
		for wall in self.list_of_collision_rects:
			if gc.pygame.Rect.colliderect(next_rect, wall):
				return wall
		return None

	def get_direction_facing(self):
		match self.current_state:
			case self.stationary:
				pass
			case (
				self.up | self.down | self.left | self.right |
				self.upleft | self.upright | self.downleft | self.downright
			):
				self.current_direction_facing = self.current_state

	def get_entity_facing(self):
		(facing_x, facing_y) = self.next_coordinates(
			self.current_direction_facing
		)
		facing_rect = gc.pygame.Rect(
			facing_x, facing_y, 
			self.puppet.height, self.puppet.width
		)
		for entity in self.list_of_entities:
			if getattr(entity, "interactable", False) and \
			(entity in self.list_of_npcs or \
			entity in self.list_of_items_on_ground):
				if gc.pygame.Rect.colliderect(facing_rect, entity):
					return entity
		return None


	def pick_up(self, item):
		item.x = None
		item.y = None
		item.rect = None
		item.visible_on_world_map = False
		self.list_of_items_on_ground.remove(item)
		if hasattr(self.puppet, "inventory"):
			self.puppet.inventory.append(item)
		# TODO: (Maybe) make a message that says "You picked up the 
		# sword!" It's "maybe" because with sprites, this will be not as
		# necessary.


		

	def handle_pygame_events(self, pygame_event):
		if pygame_event.type == gc.KEYDOWN:
			if pygame_event.key in gc.UP:
				self.send("press_up")
			if pygame_event.key in gc.DOWN:
				self.send("press_down")
			if pygame_event.key in gc.LEFT:
				self.send("press_left")
			if pygame_event.key in gc.RIGHT:
				self.send("press_right")
		if pygame_event.type == gc.KEYUP:
			# Inside this block, the checks to see if keys are pressed 
			# down allows you to wiggle-move by holding a direction and 
			# tapping the opposite.
			check = gc.pygame.key.get_pressed()
			if pygame_event.key in gc.UP:
				self.send("release_up")
				for key in gc.DOWN:
					if check[key]: self.send("press_down")
			if pygame_event.key in gc.DOWN:
				self.send("release_down")
				for key in gc.UP: 
					if check[key]: self.send("press_up")
			if pygame_event.key in gc.LEFT:
				self.send("release_left")
				for key in gc.RIGHT:
					if check[key]: self.send("press_right")
			if pygame_event.key in gc.RIGHT:
				self.send("release_right")
				for key in gc.LEFT:
					if check[key]: self.send("press_left")

	def update(self):
		# The current_frame_obstructions prevent you from moving into 
		# walls. The previous_frame_obstructions check if you have 
		# recently moved clear of a wall. If so, then you can resume 
		# moving diagonally if you are still holding that direction.
		# SIDE EFFECT: If you're running into a wall, continue to hold
		# that direction, and then press the opposite direction, then
		# you'll move clear and immediately move back, because the 
		# previous_frame_obstruction check goes through. This doesn't
		# mesh with the rest of the game, where "most recently pressed
		# direction" wins, but it's minor enough I'm not addressing at
		# this time.
		check = gc.pygame.key.get_pressed()
		self.current_frame_obstruction_up    = self.next_wall(self.up)
		self.current_frame_obstruction_down  = self.next_wall(self.down)
		self.current_frame_obstruction_left  = self.next_wall(self.left)
		self.current_frame_obstruction_right = self.next_wall(self.right)
		if self.current_frame_obstruction_up is not None:
			self.send("obstruction_up")
		elif self.previous_frame_obstruction_up is not None:
			for key in gc.UP:
				if check[key]: self.send("press_up")
		if self.current_frame_obstruction_down is not None:
			self.send("obstruction_down")
		elif self.previous_frame_obstruction_down is not None:
			for key in gc.DOWN:
				if check[key]: self.send("press_down")
		if self.current_frame_obstruction_left is not None:
			self.send("obstruction_left")
		elif self.previous_frame_obstruction_left is not None:
			for key in gc.LEFT:
				if check[key]: self.send("press_left")
		if self.current_frame_obstruction_right is not None:
			self.send("obstruction_right")
		elif self.previous_frame_obstruction_right is not None:
			for key in gc.RIGHT:
				if check[key]: self.send("press_right")
		self.previous_frame_obstruction_up    = \
			self.current_frame_obstruction_up
		self.previous_frame_obstruction_down  = \
			self.current_frame_obstruction_down
		self.previous_frame_obstruction_left  = \
			self.current_frame_obstruction_left
		self.previous_frame_obstruction_right = \
			self.current_frame_obstruction_right

		# Given all of the above collision checking, your current state
		# should be the total of the directions you are pressing and the 
		# non-obstructed directions. Thus we can move simply by using 
		# the current_state.
		(self.puppet.x, self.puppet.y) = self.next_coordinates(
			self.current_state
		)
		# Call this function after all the collision checking. 
		self.get_direction_facing()
		# Make sure to update the rect, not just the x and y 
		# coordinates.
		if hasattr(self.puppet, "rect"):
			self.puppet.rect=gc.pygame.Rect(
				self.puppet.x, self.puppet.y, 
				self.puppet.width, self.puppet.height
			)


