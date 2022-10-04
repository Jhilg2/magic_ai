from re import L

from numpy import False_
from card import Battlefield, Creature, Land, Player
from card import Card
from card import Type
from copy import deepcopy
from typing import List
from itertools import chain, combinations

def main():
	player1 = Player()
	player2 = Player()

	count = 0
	# player1.battlefield.play_land(Land("Forest"))
	# player1.battlefield.play_land(Land("Forest"))
	# player1.battlefield.play_land(Land("Forest"))
	# player1.battlefield.play_land(Land("Forest"))
	while(count < 5):
		print("======== Turn " + str(count) + " begins ========")
		print(False if count == 0 else True)
		starting_phase(player1, False if count == 0 else True)
		print("Player 1's hand")
		display_cards(player1.hand)
		play_cards(player1)
		attacks = attack(player1.battlefield)
		blocks = block(player2.battlefield, attacks)
		damage(player2, attacks, blocks)
		clean_up([player1, player2])
	
		starting_phase(player2, True)
		print("Player 2's hand")
		display_cards(player2.hand)
		play_cards(player2)
		attacks = attack(player2.battlefield)
		blocks = block(player1.battlefield, attacks)
		damage(player1, attacks, blocks)
		clean_up([player2, player1])
		count += 1
		



def clean_up(players: List[Player]):
	for player in players:
		to_destroy = []
		count = 0
		for i in range(len(player.battlefield.creatures) - 1, -1, -1):
			element = player.battlefield.creatures[i]
			if element.toughness() <= element.damage:
				player.battlefield.graveyard.append(player.battlefield.creatures.pop(i))


def damage(player: Player, attacks: List[Creature], blocks: List[List[Creature]]):
	for i in range(len(attacks)):
		if blocks[i] == []:
			attacks[i].deal_damage(player) # TODO Make damage apply to both
		else:
			attacks[i].deal_damage(blocks[i])
			for blocker in blocks[i]:
				blocker.deal_damage(attacks[i])

def starting_phase(player: Player, draw: bool = False):
	if draw:
		player.draw(1)
	player.battlefield.untap_step()
	player.battlefield.upkeep()

def play_cards(player: Player):
	played_land = False
	while True:
		plays = get_valid_plays(player, played_land)
		plays.append("End phase")
		display_cards(plays, True)
		index = int(input("select the play: "))
		to_play = plays.pop(index)
		if (isinstance(to_play, str)):
			return
		card = player.hand.pop(player.hand.index(to_play))
		if (card.get_type() == Type.LAND and not played_land):
			played_land = True
			player.battlefield.play_land(card)
		elif (card.get_type() == Type.CREATURE and card.cost() <= player.battlefield.get_available_mana()):
			player.battlefield.play_creature(card)


def powerset(l: List):
    return list(chain.from_iterable(combinations(l, r) for r in range(len(l)+1)))

def get_valid_plays(player: Player, played_land: bool):
	hand = player.hand
	landless_hand = [card for card in hand if card.get_type() != Type.LAND]
	available_mana = player.battlefield.get_available_mana()
	landless_hand.sort(key=lambda x:x.cost())
	possible_cards = [card for card in landless_hand if card.cost() <= available_mana]
	if (len(landless_hand) < len(hand) and not played_land):
		possible_cards.append(Card("Forest"))
	return deepcopy(possible_cards)

def attack(battlefield: Battlefield) -> List[Creature]:
	creatures = [creature for creature in battlefield.creatures if not creature.tapped and not creature.summoning_sick] #TODO Maybe move into Battlefield?
	print("cards without summoning sickness")
	display_cards(creatures, True)
	indices_string = input("Input the array selecting creatures to attack with ('0,1,4,5'): ")
	if not (indices_string == ''):
		indices = [eval(i) for i in indices_string.split(',')]
	else:
		return []
	return [creatures[index] for index in indices]

def block(battlefield: Battlefield, attacks: List[Creature]) -> List[List[Creature]]: #TODO add illegal blocks checks
	if len(attacks) == 0:
		return []
	print("Here are the opponents attacks:")
	display_cards(attacks, True)
	print("Here are your possible blockers:")
	blockers = [creature for creature in battlefield.creatures if not creature.tapped] #TODO Maybe move into Battlefield?
	display_cards(blockers, True)
	indices_string = input("enter a list of lists of the blockers for each attacker ('0:3:2,1::4'): ")
	if not (indices_string == ''):
		return [[blockers[eval(i)] for i in group.split(',')] if not (group == '') else [] for group in indices_string.split(':')]
	return []

def display_cards(cards: List[Card], indices: bool = False):
	if indices:
		for i in range(len(cards)):
			print(str(i) + ": " + str(cards[i]))
	else:
		[print(card) for card in cards]


if __name__ == "__main__":
	main()
