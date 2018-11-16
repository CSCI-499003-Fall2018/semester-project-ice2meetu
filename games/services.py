import random
from creation.models import Event, EventUser, Group, Grouping
from .utils import _replace, max_groups, _random_grps

class SimulatedAnnealing:
    def __init__(self, event):
        self.event = event

        # cleanup before starting
        all_groupings = list(event.grouping_set.all())
        for grouping in all_groupings:
            grouping.delete()
        
        self.players = {user.pk for user in event.users()}
        self.max_groups = 0
        if len(self.players) < 10:
            self.max_groups = max_groups(len(self.players))
        else:
            self.max_groups = float('inf')
        
        self.start_state = self.random_groups() #random grouping
    
    def random_groups(self):
        if self.event.user_count() != len(self.players):
            self.players = {user.pk for user in event.users()}
        event_users = self.players
        groupings_ids = _random_grps(event_users)
        grouping = Grouping(event=self.event, is_current=True)
        grouping.save()
        for group in groupings_ids:  # make group for grouping
            g = Group(grouping=grouping)
            for user_id in group:  # add user to group
                g.save()
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
