from enum import Enum

TURN_LIMIT: int = 5

class Phase(Enum):
    PLAY = 0
    ATTACK = 1
    BLOCK = 2

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