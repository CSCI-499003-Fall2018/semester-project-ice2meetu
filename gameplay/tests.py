from django.test import TestCase
from .models import GameManager, Player
from creation.models import Event, EventUser, Grouping, Group

class GameManagerTestCase(TestCase):
    fixtures = ['db-creation.json', 'db-games.json', 'db-user.json']

    def setUp(self):
        event = Event.objects.get(pk=2)
        grouping1 = Grouping.objects.create(event=event, is_current=False)
        grouping2 = Grouping.objects.create(event=event, is_current=True)
        GameManager.objects.create(event=event)
    
    def test_initial_state(self):
        """Tests signal that cleans event of previous groupings and
        tests that GameManager doesn't have players upon init"""
        manager = GameManager.objects.all()[0]
        self.assertFalse(manager.event.grouping_set.exists())
        self.assertFalse(manager.player_set.exists())

    def test_add_players(self):
        """Tests adding players"""
        manager = GameManager.objects.all()[0]
        eventusers = list(manager.event.users())
        manager.add_player(eventusers[0])
        manager.add_player(eventusers[1])

        self.assertEqual(manager.player_set.count(), 2)
        self.assertEqual(len(manager.players()), 2)
        self.assertIn(eventusers[0].pk, manager.players())
        self.assertIn(eventusers[1].pk, manager.players())
    
    def test_remove_players(self):
        """Tests removing players"""
        manager = GameManager.objects.all()[0]
        eventusers = list(manager.event.users())
        manager.add_player(eventusers[0])
        manager.add_player(eventusers[1])
        manager.remove_player(eventusers[0])
        manager.remove_player(eventusers[1])
        
        self.assertNotIn(eventusers[0].pk, manager.players()
        self.assertEqual(manager.player_set.count(), 0)
        self.assertEqual(len(manager.players()), 0)
    
    def test_sync_users(self):
        """Tests adding all event users to the game"""
        manager = GameManager.objects.all()[0]
        manager.sync_users()
        eventusers = {user.pk for user in manager.event.users()}
        count = len(eventusers)
        self.assertEqual(manager.player_set.count(), count)
        self.assertEqual(len(manager.players()), count)
        self.assertCountEqual(manager.players(), eventusers)




        

        
    
