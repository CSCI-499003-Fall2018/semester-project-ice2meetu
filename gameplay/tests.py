from django.test import TestCase
from .models import GameManager, Player
from creation.models import Event, EventUser, Grouping, Group

class GameManagerUserTestCase(TestCase):
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

        self.assertNotIn(eventusers[0].pk, manager.players())
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
    
    
class GameManagerPlayTestCase(TestCase):
    fixtures = ['db-creation.json', 'db-games.json', 'db-user.json']

    def setUp(self):
        event = Event.objects.get(pk=2)
        manager = GameManager.objects.create(event=event)

        # add players to the game
        eventusers = list(manager.event.users())
        for user in eventusers[:5]:
            manager.add_player(user)
    
    def test_random_grouping(self):
        """Tests random grouping and get_current_grouping functions"""
        manager = GameManager.objects.all()[0]

        manager.random_groups()
        grouping = manager.event.grouping_set.filter(is_current=True)
        self.assertTrue(grouping.exists())  # grouping created
        self.assertEqual(manager.get_current_grouping(), grouping[0])
        self.assertTrue(len(grouping[0].groups()) >= 1)  # with at least one group

        count = 0
        for group in grouping[0].groups():
            count += group.size()
        self.assertEqual(count, 5)

    def test_find_duplicate_groups(self):
        """Tests getting duplicate groups in a grouping (search group history)"""
        manager = GameManager.objects.all()[0]

        manager.random_groups()
        curr_group = manager.event.grouping_set.filter(is_current=True)[
            0].groups()[0]
        manager.event.save_group_history()
        grouping = Grouping(event=manager.event)
        grouping.save()
        group = Group(grouping=grouping)
        group.save()

        for user in curr_group.users():
            group.eventuser_set.add(user)
        group.save()

        # check if duplicate grouping was successfully created
        self.assertEqual(curr_group, group)

        duplicates = manager._find_duplicate_groups(grouping)

        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0], curr_group)
    
    def test_generate_groups(self):
        """Tests generating groups for rounds"""
        manager = GameManager.objects.all()[0]
        event = manager.event
        prev_history_count = -1 # num groups in event's history, previously

        # do not exceed 11, manager.max_groups is set by higher level func
        for i in range(11):
            generated = manager._generate()
            curr_grouping = manager.event.grouping_set.filter(is_current=True)[
                0]         

            curr_history_count = len(event.get_grouping_hist().groups())
            self.assertTrue(curr_history_count > prev_history_count)
            self.assertEqual(generated, curr_grouping)
            prev_history_count = len(event.get_grouping_hist().groups())



        

        
    
