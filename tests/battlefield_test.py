import unittest
from card import Creature, Land, Card
from battlefield import Battlefield

class TestBattlefield(unittest.TestCase):
    
    def setUp(self):
        self.battlefield = Battlefield()
        # Create mock Land and Creature objects as needed for testing
        self.land1 = Land("Forest")  # Assuming Land class has a default constructor
        self.land2 = Land("Forest")
        self.land3 = Land("Forest")
        self.bear = Creature("Bear Cub")
        self.frillback = Creature("Orazca Frillback")

        # Mock the necessary methods for land and creature objects
        
        self.bear.summoning_sick = False

        self.frillback.summoning_sick = False

    def test_play_land(self):
        self.battlefield.play_land(self.land1)
        self.assertIn(self.land1, self.battlefield.lands)
        
        self.battlefield.play_land(self.land2)
        self.assertIn(self.land2, self.battlefield.lands)
        self.assertEqual(len(self.battlefield.lands), 2)

    def test_play_creature_success(self):
        self.battlefield.play_land(self.land1)
        self.battlefield.play_land(self.land2)
        self.battlefield.play_land(self.land3)
        self.battlefield.play_creature(self.bear)
        self.assertIn(self.bear, self.battlefield.creatures)
        self.assertFalse(self.land3.tapped)

    def test_play_creature_failure(self):
        # Not enough lands to play creature
        self.assertFalse(self.battlefield.play_creature(self.frillback))
        self.assertNotIn(self.frillback, self.battlefield.creatures)

    def test_tap_lands(self):
        self.battlefield.play_land(self.land1)
        self.battlefield.play_land(self.land2)
        self.battlefield.tap_lands(1)
        self.assertTrue(self.land1.tapped)
        self.assertFalse(self.land2.tapped)

    def test_get_available_mana(self):
        self.battlefield.play_land(self.land1)
        self.battlefield.play_land(self.land2)
        self.assertEqual(self.battlefield.get_available_mana(), 2)
        
        # Tap a land and check mana again
        self.land1.tapped = True
        self.assertEqual(self.battlefield.get_available_mana(), 1)

    def test_get_attacks(self):
        self.bear.summoning_sick = True
        for x in range(10):
            self.battlefield.play_land(Land("Forest"))
        self.battlefield.play_creature(self.bear)
        self.battlefield.play_creature(self.frillback)
        self.assertIn(self.frillback, self.battlefield.get_attacks())

    def test_attack(self):
        self.battlefield.play_creature(self.bear)
        damage = self.battlefield.attack([self.bear])
        self.assertEqual(damage, 2)

    def test_untap_step(self):
        self.battlefield.play_land(self.land1)
        self.battlefield.play_creature(self.bear)

        # Tap cards before untap step
        self.land1.tapped = True
        self.bear.tap()

        self.battlefield.untap_step()

        # Check that they are untapped
        self.assertFalse(self.land1.tapped)
        self.assertFalse(self.bear.summoning_sick)

    def test_upkeep(self):
        self.bear.summoning_sick = True
        self.battlefield.creatures.append(self.bear)

        self.battlefield.upkeep()

        # Summoning sickness should be removed
        self.assertFalse(self.bear.summoning_sick)

if __name__ == '__main__':
    unittest.main()
