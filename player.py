import random
from battlefield import Battlefield
from constants import BASE_DECK
from card import Card

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