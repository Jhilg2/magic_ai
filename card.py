from typing import List, Union
from constants import Type, CARDS

class Card(object):
	"""docstring for card."""

	def __init__(self, name):
		super(Card, self).__init__()
		self.name = name
		self.info = CARDS[self.name]
		self.tapped = False


	def __str__(self):
		# return "Card.get_card('" + self.name + "')"
		return self.name + ": " + str(CARDS[self.name]["cost"])
	
	def __eq__(self, other):
		return isinstance(other, Card) and self.name == other.name
	__repr__ = __str__

	@staticmethod
	def get_card(name):
		card_type = CARDS[name]["type"]
		if card_type == Type.CREATURE:
			return Creature(name)
		elif card_type == Type.LAND:
			return Land(name)

	def tap(self):
		success = not (self.tapped)
		self.tapped = True
		return success
	
	def untap(self):
		self.tapped = False

	def get_info(self):
		return CARDS[self.name]

	def get_type(self):
		return self.info["type"]

	def cost(self):
		return self.info["cost"]

class Land(Card):
	"""docstring for land."""

	def __str__(self):
		return self.name + ": " + ("tapped" if self.tapped else "untapped")

	__repr__ = __str__

	def __init__(self, name):
		super().__init__(name)


class Creature(Card):
	
	def __init__(self, name):
		super().__init__(name)
		self.summoning_sick = True
		self.damage = 0
	
	def __str__(self):
		return self.name + ": " + str(self.cost()) + " (" + str(self.power()) + "/" + str(self.toughness()) + ")"

	__repr__ = __str__

	def power(self):
		return self.info["power"]

	def toughness(self):
		return self.info["toughness"]

	def remove_summoning_sickness(self):
		self.summoning_sick = False

	def take_damage(self, damage: int):
		self.damage += damage

	def deal_damage(self, target: Union[List['Creature'],'Player']):
		total_damage = self.power()
		if isinstance(target, list):
			i = 0
			while total_damage > 0 and len(target) > 0 and i < len(target):
				if target[i].toughness() < total_damage:
					target[i].take_damage(target[i].toughness())
					total_damage -= target[i].toughness()
				else:
					target[i].take_damage(total_damage)
					total_damage = 0
				i += 1
			if total_damage > 0 and len(target) > 0:
				target[-1].take_damage(total_damage)
		else:
			target.take_damage(total_damage)
