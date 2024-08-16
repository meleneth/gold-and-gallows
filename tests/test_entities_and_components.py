from gng.entities_and_components \
import Entity, create_item, create_player, create_npc

def create_test_player():
	return create_player(
		name="player", 
		CHA=20, CON=20, DEX=20, INT=20, STR=20, WIS=20, 
		max_HP=10, AC=10, AV=10
	)

def create_test_potato():
	return create_npc(
		name="potato", 
		x=10, y=10, width=30, height=30, 
		level=42, dialogue_tree=None
	)

def create_test_sword():
	return create_item(
		"sword", equippable=True, slot="held_slot", damage_die=4, AC_value=0
	)

def test_creating_sword_player_potato():
	sword=create_test_sword()
	player=create_test_player()
	potato=create_test_potato()

def test_sword_can_be_equipped():
	sword=create_test_sword()
	player=create_test_player()
	player.equip(sword)
	assert sword in player.held_slot

def test_entities_without_equip_method_cannot_equip_an_item():
	sword=create_test_sword()
	try:
		sword.equip(sword)
	except Exception:
		assert True
		return
	assert False

def test_attack_with_sword():
	pass
	