from card import Creature, Land, Card
from typing import List

class Battlefield(object):
	
	def __init__(self):
		super(Battlefield, self).__init__()
		self.lands: List[Land]  = []
		self.creatures: List[Creature] = []
		self.graveyard: List[Card] = []
	
	def __str__(self):
		s = "Creatures:\n"
		s += str([creature for creature in self.creatures]) + "\n"
		s += "Lands:\n"
		s += str([land for land in self.lands]) + "\n"
		s += "Graveyard:\n"
		s += str([card for card in self.graveyard]) + "\n"
		return s

	__repr__ = __str__

	def play_land(self, card: Land):
		self.lands.append(card)
	
	def get_available_mana(self):
		# print("get_available_mana:")
		# print([land for land in self.lands])
		return len([land for land in self.lands if not land.tapped])
	
	def play_creature(self, card: Creature):
		if card.cost() > self.get_available_mana():
			return False
		self.creatures.append(card)
		self.tap_lands(card.cost())
		# print(self.creatures)
	
	def tap_lands(self, lands_to_tap: int):
		x = lands_to_tap
		for land in self.lands:
			if x > 0 and land.tap():
				x -= 1

	def get_attacks(self):
		return [card for card in self.creatures if not card.summoning_sick]

	def attack(self, attack_array: List[Creature]) -> int:
		damage = []
		for creature in attack_array:
			creature.tap()
			damage.append(creature.power())
		return sum(damage)

	def untap_step(self):
		for card in self.lands:
			card.untap()
		for card in self.creatures:
			card.untap()

	def upkeep(self):
		for card in self.creatures:
			card.remove_summoning_sickness()