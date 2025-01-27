from functools import partial

import gng.dice_roller      as dr
import gng.global_constants as gc

class NoSlotDefined(Exception):
	pass

class NotEquippable(Exception):
	pass

class UnreachableDialogue(Exception):
	pass

# ----------------------------------------------------------------------

# This code lets us define an indeterminate amount of components when we 
# instantiate an object of Entity. You can also add new components to an 
# Entity after creation by simply declaring them (e.g., Bob.x = 5 makes 
# Bob have an attribute of x with value 5 _even if_ Bob previously did 
# not have an attribute of x.

class Entity:
	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)

def create_item(name, equippable=False, slot="", damage_die=0, AC_value=0):
	entity = Entity()
	give_name_component(entity, name)
	give_item_component(
		entity, equippable, slot, damage_die, AC_value
	)
	return entity

def create_player(name, CHA, CON, DEX, INT, STR, WIS, max_HP, AC, AV):
	entity = Entity()
	give_name_component(entity, name)
	give_equipment_component(entity)
	give_world_map_component(
		entity, 
		x=0, y=0, 
		width=30, height=30, 
		color=gc.BLUE, 
		visible_on_world_map=True, interactable=False
	)
	give_player_stats_component(
		entity, CHA, CON, DEX, INT, STR, WIS, max_HP, AC, AV
	)
	give_moveable_component(entity, speed=4)
	give_level_component(entity, level=1)
	return entity

def create_npc(name, x, y, width, height, HD, dialogue_tree):
	entity = Entity()
	give_name_component(entity, name)
	give_moveable_component(entity, speed=4)
	give_equipment_component(entity)
	give_world_map_component(entity, x, y, width, height, color=gc.GREEN)
	give_HD_component(entity, HD)
	give_dialogue_component(entity, dialogue_tree)
	return entity



# ----------------------------------------------------------------------

def give_world_map_component(
	entity, x, y, width, height, color,
	visible_on_world_map=True, interactable=True
):
	entity.x = x
	entity.y = y
	entity.width = width
	entity.height = height
	entity.color = color
	entity.rect = \
		gc.pygame.Rect(x, y, width, height)
	entity.visible_on_world_map = visible_on_world_map
	entity.interactable = interactable

def give_item_component(
	entity, equippable=False, slot="", damage_die=0, AC_value=0, 
):
	if equippable and slot=="":
		raise NoSlotDefined("An equippable item must have a slot.")
	entity.equippable = equippable
	entity.slot = slot
	entity.damage_die = damage_die
	entity.AC_value = AC_value

def give_name_component(entity, name):
	entity.name = name

def give_equipment_component(
	entity,
	inventory=[],
	held_slot=[], # Max size: number_of_arms
	glove_slot=[], # Max size: number_of_arms
	number_of_arms=2,
	head_slot=[], # Max size: number_of_heads
	necklace_slot=[], # Max size: number_of_heads
	number_of_heads=1,
	boot_slot=[], # Max size: number_of_legs
	number_of_legs=2,
	ring_slot=[], # Max size: number_of_fingers
	number_of_fingers_on_a_hand=5,
	armor_slot=[], # Max size: number_of_torsos
	back_slot=[], # Max size: number_of_torsos
	number_of_torsos=1,
):
	entity.inventory = inventory
	entity.held_slot = held_slot
	entity.glove_slot = glove_slot
	entity.number_of_arms = number_of_arms
	entity.head_slot = head_slot
	entity.necklace_slot = necklace_slot
	entity.number_of_heads = number_of_heads
	entity.boot_slot = boot_slot
	entity.number_of_legs = number_of_legs
	entity.ring_slot = ring_slot
	entity.number_of_fingers_on_a_hand = number_of_fingers_on_a_hand
	entity.armor_slot = armor_slot
	entity.back_slot = back_slot
	entity.number_of_torsos = number_of_torsos

	def equip(self, item):
		if item.equippable:
			slot_string = item.slot
			slot_list = getattr(self, slot_string)
			slot_list.append(item)
		else:
			raise NotEquippable("That item is not equippable.")
	entity.equip = partial(equip, entity)

def give_dialogue_component(entity, dialogue_tree):
	if not entity.interactable:
		raise UnreachableDialogue(
			"An entity with a dialogue tree that "\
			"can't be interacted with will never display its dialogue."
		)
	entity.dt = dialogue_tree

def give_moveable_component(entity, speed):
	entity.speed = speed

def give_player_stats_component(
	entity, CHA, CON, DEX, INT, STR, WIS, max_HP, AC, AV
):
	entity.CHA = CHA
	entity.CON = CON
	entity.DEX = DEX
	entity.INT = INT
	entity.STR = STR
	entity.WIS = WIS
	entity.max_HP = max_HP
	entity.HP = entity.max_HP
	entity.AC = AC
	entity.AV = AV

	def attacks(self, enemy):
		weapon = entity.held_slot[0] # TODO: how do I reconcile multiple or no weapons?
		if dr.thread_the_needle(enemy.HD, entity.AV):
			weapon.damages(enemy)
	entity.attacks = partial(attacks, entity)

	def defends(self, enemy):
		pass
	entity.defends = partial(defends, entity)


def give_level_component(entity, level):
	entity.level = level

def give_HD_component(entity, HD):
	entity.HD = HD
	# By defining a HD (hit die), you can derive all other values. They 
	# can be overridden on a case-by-case basis when desired.
	entity.max_HP = round(entity.HD * gc.AVERAGE_HP_PER_HD)
	entity.HP = entity.max_HP

def give_damage_dealing_component(entity, damage_die):
	entity.damage_die = damage_die

	def damages(self, entity):
		damage_roll = dr.roll_x_d_n(1, self.damage_die)
		entity.HP -= damage_roll
	entity.damages = partial(damages, entity)
