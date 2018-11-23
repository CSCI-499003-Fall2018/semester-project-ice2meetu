import random

def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0


def max_groups(num_players):
    """Return max number of groupings before groups have to repeat"""
    if num_players == 2 or num_players == 3:
        return 1
    if num_players > 8: #thousands of grps available
        return float("inf") #so return infinity
    maxn = 0
    for i in range(num_players//2 + 1):
        if i == (num_players-1) or i == 1:
            continue
        if i == 0 and num_players <= 9:
            maxn += 1
        else:
            # eliminate complementary chooses, so halve 4C2, 6C3, etc.
            comb = (choose(num_players, i) if (i != num_players / 2)
                    else choose(num_players, i) // 2)
            maxn += comb * max_groups(num_players-i)
    return maxn


def _random_grps(players_set, grouped=None):
    """
    Returns a randomized list of groups from a list of player id's
    """
    players = players_set.copy()
    if len(players) == 1:
        return []
    if len(players) == 3:
        try:
            grouped.append(players)
        except AttributeError:
            grouped = [players]
        return grouped
    if not players:
        return grouped

    max_players = 10 if len(players) > 9 else len(players) + 1
    grp_size = random.randrange(2, max_players)
    # choose random numbers until grp_size valid
    while (len(players) - grp_size == 1):
        grp_size = random.randrange(2, max_players)

    group = set(random.sample(players, grp_size))
    if not grouped:
        grouped = [group]
    else:
        grouped.append(group)
    return _random_grps(players.difference(group), grouped)
