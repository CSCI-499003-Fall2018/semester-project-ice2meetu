from django.test import TestCase
from .models import GameManager, Player
from django.contrib.auth.models import User
from creation.models import Event, EventUser, Grouping, Group
from creation.utils import genAccessCode
from functools import reduce
import random

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
        manager.remove_player(eventusers[0].player)
        manager.remove_player(eventusers[1].player)
        
        self.assertFalse(eventusers[0].is_playing())
        self.assertFalse(eventusers[1].is_playing())
        self.assertNotIn(eventusers[0].pk, manager.players())
        self.assertEqual(manager.player_set.count(), 0)
        self.assertEqual(len(manager.players()), 0)
    

    def test_sync_users(self):
        """Tests adding all event users to the game"""
        manager = GameManager.objects.all()[0]
        eventusers = list(manager.event.users())
        manager.add_player(eventusers[0])
        manager.add_player(eventusers[1])
        manager.sync_users()
        eventusers = {user.pk for user in manager.event.users()}
        count = len(eventusers)
        self.assertEqual(manager.player_set.count(), count)
        self.assertEqual(len(manager.players()), count)
        self.assertCountEqual(manager.players(), eventusers)
        self.assertNotEqual(manager.max_groups, 100)
    
    
class GameManagerPlayTestCase(TestCase):
    fixtures = ['db-creation.json', 'db-games.json', 'db-user.json']

    def setUp(self):
        title = 'Thwackathon: Thwacking Contest'
        admin = User.objects.get(pk=1)
        event = Event.objects.create(title=title, admin=admin,  
                                     event_type='Hackathon', 
                                     access_code=genAccessCode())
        manager = GameManager.objects.create(event=event)

        # add players to the game
        test_users = random.sample(Event.objects.get(pk=2).users(), 5)
        for user in test_users[:5]:
            user.events.add(event)
            manager.add_player(user)
    

    def test_random_grouping(self):
        """Tests random grouping and get_current_grouping functions"""
        manager = GameManager.objects.all()[0]

        manager.random_groups()
        grouping = manager.event.grouping_set.filter(is_current=True)
        self.assertTrue(grouping.exists())  # grouping created
        self.assertEqual(manager.get_current_grouping(), grouping[0])
        self.assertTrue(len(grouping[0].groups()) >= 1)  # with at least one group

        player_count = reduce(lambda x, grp: x + grp.size(), 
                              grouping[0].groups(), 0)
        self.assertEqual(player_count, 5)


    def test_find_duplicate_groups(self):
        """Tests getting duplicate groups in a grouping (search group history)"""
        manager = GameManager.objects.all()[0]

        manager.random_groups()
        event = manager.event
        curr_group = manager.get_current_grouping().groups()[0]
        manager.event.save_group_history()
        grouping = Grouping(event=manager.event, is_current=True)
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
        # num groups in event's history, previously
        prev_history_count = -1 

        for i in range(11):
            generated = manager._generate()
            curr_grouping = manager.event.grouping_set.filter(is_current=True)[
                0]         

            curr_history_count = len(event.get_grouping_hist().groups())
            self.assertTrue(curr_history_count > prev_history_count)
            self.assertEqual(generated, curr_grouping)
            prev_history_count = len(event.get_grouping_hist().groups())
    

    def test_play(self):
        """Tests go_round function: initiates and continues event play"""
        manager = GameManager.objects.all()[0]
    
        def check_games(self, manager):
            grouping = manager.get_current_grouping()
            for group in grouping.groups():
                self.assertTrue(group.game)

        for i in range(11):
            play = manager.go_round()
            if i == 0:
                self.assertTrue(manager.event.is_playing)
                self.assertNotEqual(manager.max_groups, 100)
            manager.get_current_grouping()
            self.assertTrue(play)
            self.assertEqual(manager.round_num, i+1)
            check_games(self, manager)
        
        self.assertFalse(manager.go_round()) #exceeds max
    

    def test_add_remove_ingame(self):
        """Tests adding/removing players in between rounds"""
        manager = GameManager.objects.all()[0]

        def add(x, y):
            if isinstance(x, Group):
                print("x is a Group: {}".format(x))
                return x.size() + y.size()
            else:
                print("x is an int: {}".format(x))
                return x + y.size()

        def count_grouped_players(manager):
            grouping = manager.get_current_grouping()
            count = reduce(
                lambda x, grp: x + grp.size(), grouping.groups(), 0)
            return count
        
        # 5 players --> 3 players
        players = list(manager.player_set.all())
        manager.remove_player(players[0])
        manager.remove_player(players[1])

        play = manager.go_round()
        grouped_count = count_grouped_players(manager)
        self.assertEqual(grouped_count, 3)
        self.assertEqual(manager.max_groups, 1)
        
        # 3 players --> 5 players
        manager.sync_users()
        play = manager.go_round()
        grouped_count = count_grouped_players(manager)
        self.assertEqual(grouped_count, 5)
        self.assertEqual(manager.max_groups, 11)


    def test_end(self):
        """Tests ending the game"""
        manager = GameManager.objects.all()[0]
        event = manager.event
        event_users = event.users()

        play = manager.go_round()
        manager.end_game()
        self.assertFalse(event.is_playing)
        self.assertFalse(GameManager.objects.all().exists())
        for user in event_users:
            self.assertFalse(user.is_playing())