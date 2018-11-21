import random
from creation.models import Event, EventUser, Group, Grouping
from .models import Game
from .utils import max_groups, _random_grps

# randomly picks a game for each group in grouping
def start_games(grouping):
    for group in grouping.groups():
        nplayers = group.size()
        filtered_games = Game.objects.nplayer_games(nplayers)
        group.game = random.choice(list(filtered_games))
        group.save()


class SimulatedAnnealing:
    def __init__(self, event):
        self.event = event

        # cleanup before starting
        all_groupings = list(event.grouping_set.all())
        for grouping in all_groupings:
            grouping.delete()
        
        self.players = {user.pk for user in event.users()}
        nplayers = len(self.players)
        self.max_groups = max_groups(nplayers) if nplayers < 10 else float('inf')
        self.start_state = self.random_groups() #random grouping
    
    # for in round adding and removing players
    def remove_user(self, eventuser):
        pk = eventuser if isinstance(eventuser,int) else eventuser.pk
        self.players.discard(pk)
    
    def add_user(self, eventuser):
        pk = eventuser if isinstance(eventuser, int) else eventuser.pk
        if pk in {user.pk for user in self.event.users()}:
            self.players.add(pk)
        else:
            raise AttributeError("Player {} is not a user registered for this event".format(pk))
    
    def sync_users(self):
        if self.event.user_count() != len(self.players):
            self.players = {user.pk for user in self.event.users()}
    
    def random_groups(self):
        event_users = self.players
        groupings_ids = _random_grps(event_users)
        grouping = Grouping(event=self.event, is_current=True)
        grouping.save()
        for group in groupings_ids:  # make group for grouping
            g = Group(grouping=grouping)
            g.save()
            for user_id in group:  # add user to group
                g.eventuser_set.add(EventUser.objects.get(pk=user_id))
        return grouping
    
    def _find_duplicate_groups(self, grouping):
        past_groups = self.event.get_grouping_hist().groups()
        current_groups = grouping.groups()
        duplicate_groups = []
        for group in current_groups:
            if group in past_groups:
                duplicate_groups.append(group)
        return duplicate_groups

    def generate(self):
        yield self.start_state
        while self.event.get_grouping_hist().size() < self.max_groups:
            if self.event.has_current_grouping():
                self.event.save_group_history()
            new_grouping = self.random_groups()
            duplicate_groups = self._find_duplicate_groups(new_grouping)
            while duplicate_groups:
                if len(duplicate_groups) >= 2:
                    group1, group2 = random.sample(duplicate_groups, 2)
                else:
                    group1 = duplicate_groups[0]
                    group2 = random.choice(new_grouping.groups())
                new_grouping.random_swap(group1, group2)
                duplicate_groups = self._find_duplicate_groups(new_grouping)
            yield new_grouping
