from card import Player
from card import Card
from card import Type
from typing import List
from itertools import chain, combinations

def main():
	player1 = Player()
	# player2 = Player()
	p = powerset([1,2,3])
	for x in p:
		print(x)
	# for x in p:
	# 	if "x" in x:
	# 		print(x)
	# for x in p:
	# 	if "x" not in x:
	# 		print(x)
	
	count = 0
	# while(count < 5):
	# starting_phase(player1, False)
	player1.battlefield.play_land(Card("Forest"))
	player1.battlefield.play_land(Card("Forest"))
	player1.battlefield.play_land(Card("Forest"))
	player1.battlefield.play_land(Card("Forest"))
	print(player1.battlefield.lands)
	# print("Player 1's hand")
	# display_cards(player1.hand)
	# play_cards(player1, [1,2,3])
	count + 1

def starting_phase(player: Player, draw: bool = False):
	if draw:
		player.draw(1)
	player.battlefield.untap_step()

def play_cards(player: Player, cards_to_play: List[int] = None):
	if cards_to_play == None:
		cont = True
		played_land = False
		while cont:
			index = int(input("select the index of a card from your hand: "))
			card = player.hand.pop(index)
			info = card.get_info()
			print(info)
			print(player.battlefield.get_available_mana())
			if (info['type'] == Type.LAND and not played_land):
				player.battlefield.play_land(card)
			elif (info['type'] == Type.CREATURE and info['cost'] <= player.battlefield.get_available_mana()):
				player.battlefield.play_creature(card)
			else:
				print("You can't play that card!")
			cont = "yes" == input("Are you finished? yes/no: ")
	else:
		plays = get_valid_plays(player)
		print(plays)
		pass

def powerset(l: List):
    return list(chain.from_iterable(combinations(l, r) for r in range(len(l)+1)))

def get_valid_plays(player: Player):
	hand = player.hand
	# landless_hand = [print(card.info) for card in hand]
	landless_hand = [card for card in hand if card.get_type() != Type.LAND]
	available_mana = player.battlefield.get_available_mana()
	print(landless_hand)
	landless_hand.sort(key=lambda x:x.cost())
	have_land = len(landless_hand) < len(hand)
	possible_cards = [card for card in landless_hand if card.cost() <= available_mana + 1]
	# We have a land
	plays = powerset(possible_cards)
	pruned_plays = []
	for play in plays:
		if have_land:
			temp = pruned_plays + (Card("Forest"),)
	landless_plays = [play for play in plays if sum(card.cost() for card in play) <= available_mana + 1]
	else:
		# print("available_mana: " + str(available_mana))
		possible_cards = [card for card in landless_hand if card.cost() <= available_mana]
		# print("landless_hand:")
		# print(landless_hand)
		# print("possible_cards:")
		# print(possible_cards)
		plays = powerset(possible_cards)
		# print("plays")
		# print(plays)
		return [play for play in plays if sum(card.cost() for card in play) <= available_mana]


def display_cards(cards: List[Card]):
	[print(card) for card in cards]


if __name__ == "__main__":
	main()
