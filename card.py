from enum import Enum
import random
from typing import List, Union

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
		
class Player(object):

	def __init__(self):
		super(Player, self).__init__()
		self.life = 20
		self.deck = self._deck()
		self.hand = []
		self.mulligan(0)
		self.battlefield = Battlefield()
	
	@staticmethod
	def _deck():
		deck = []
		for card in BASE_DECK:
			deck.extend([Card.get_card(card)] * BASE_DECK[card])
		return deck

	def mulligan(self, put_on_bottom):
		random.shuffle(self.deck)
		self.draw(7)
		# self.hand = [
		# 	Card.get_card("Orazca Frillback"),
		# 	Card.get_card("Garruk's Gorehorn"),
		# 	Card.get_card("Bear Cub"),
		# 	Card.get_card("Treetop Warden"),
		# 	Card.get_card("Forest"),
		# 	Card.get_card("Forest"),
		# 	Card.get_card("Forest")
		# ]
		# TODO: add london mulligan

	def take_damage(self, damage: int):
		self.life -= damage

	def draw(self, cards_to_draw):
		self.hand.extend([self.deck.pop() for i in range(cards_to_draw)])
		

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
		print("get_available_mana:")
		print([land for land in self.lands])
		return len([land for land in self.lands if not land.tapped])
	
	def play_creature(self, card: Creature):
		if card.cost() > self.get_available_mana():
			return False
		self.creatures.append(card)
		self.tap_lands(card.cost())
		print(self.creatures)
	
	def tap_lands(self, lands_to_tap: int):
		x = lands_to_tap
		for land in self.lands:
			if x > 0 and land.tap():
				x -= 1

	def get_attacks(self):
		return [card for card in self.creatures if card.summoning_sick]

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

class Type(Enum):
	LAND = "land"
	CREATURE = "creature"

BASE_DECK = {
	"Forest": 24,
	"Bear Cub": 4,
	"Grizzly Bears": 4,
	"Treetop Warden": 4,
	"Centaur Courser": 4,
	"Orazca Frillback": 4,
	"Wild Ceratok": 4,
	"Garruk's Gorehorn": 4,
	"Grizzled Outrider": 4,
}

CARDS = {
	"Forest": { "type": Type.LAND, "cost": 0},
	"Bear Cub": { "type": Type.CREATURE, "cost": 2, "power": 2, "toughness": 2},
	"Grizzly Bears": { "type": Type.CREATURE, "cost": 2, "power": 2, "toughness": 2},
	"Treetop Warden": { "type": Type.CREATURE, "cost": 2, "power": 2, "toughness": 2},
	"Centaur Courser": { "type": Type.CREATURE, "cost": 3, "power": 3, "toughness": 3},
	"Orazca Frillback": { "type": Type.CREATURE, "cost": 3, "power": 4, "toughness": 2},
	"Wild Ceratok": { "type": Type.CREATURE, "cost": 4, "power": 4, "toughness": 3},
	"Garruk's Gorehorn": { "type": Type.CREATURE, "cost": 5, "power": 7, "toughness": 3},
	"Grizzled Outrider": { "type": Type.CREATURE, "cost": 5, "power": 5, "toughness": 5},
}
