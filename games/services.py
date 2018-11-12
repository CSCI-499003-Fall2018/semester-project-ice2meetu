import random
from creation.models import Event, EventUser, Group, Grouping
from .utils import _replace, max_groups, _random_grps

# Group Utils #
def random_groups(event):
    event_users = {user.pk for user in event.users()}
    groupings_ids = _random_grps(event_users)
    grouping = Grouping(event=event, is_current=True).save()
    for group in groupings_ids:
        g = Group(grouping=grouping)
        for user_id in group:
            g.eventuser_set.add(User.objects.get(pk=user_id))
        g.save()
    return grouping


def random_swap(group1, group2):
    player1 = random.choice(list(group1))
    player2 = random.choice(list(group2))
    # g1, g2 = group1.copy(), group2.copy()
    _replace(group1, player1, player2)
    _replace(group2, player2, player1)
    assert(g1 != group1)
    assert(g2 != group2)
    # self.checkpoint = [(g1, group1), (g2, group2)]
    
# def undo_swap(self):
#     old_g1, curr_g1 = self.checkpoint[0]
#     old_g2, curr_g2 = self.checkpoint[1]
#     _replace(self.groups, curr_g1, old_g1)
#     _replace(self.groups, curr_g2, old_g2)
#     assert(old_g1 in self.groups)
#     assert(old_g2 in self.groups)


class SimulatedAnnealing:
    def __init__(self, players_list):
        self.start_state = Groups(players_list)
        self.previous_groups = [group for group in self.start_state.groups]
        self.current_state = Groups(players_list)
        self.players = players_list
        self.max_groups = 0
        if len(players_list) < 10:
            self.max_groups = max_groups(len(self.players))
        else:
            self.max_groups = float('inf')

    def _find_non_unique(self, state):
        return [group for group in state.groups if group in self.previous_groups]

    def generate(self):
        yield self.start_state
        while len(self.previous_groups) < self.max_groups:
            new_group = Groups(self.players)
            non_unique = self._find_non_unique(new_group)
            while non_unique:
                if len(non_unique) >= 2:
                    group1, group2 = random.sample(non_unique, 2)
                else:
                    group1 = non_unique[0]
                    group2 = random.choice(new_group.groups)
                new_group.random_swap(group1, group2)
                non_unique = self._find_non_unique(new_group)
            self.current_state = new_group
            for group in new_group.groups:
                self.previous_groups.append(group)
            yield new_group
