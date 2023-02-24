"""
General ideas:
- sum of tiers of both team should be about the same
- add some randomness

PlayerRole is an object that contain an information about a player's role and corresponding tier.
Which means, a player can have multiple PlayerRole objects, one for each role.

Algorithm:
1. Sort the list of PlayerRoles by tier in descending order.
   Each team will select players based on this. Since the list is sorted by role's tier, players will have more chance to play their best roles.
2. Randomly assign one player to each team, for two reason:
   1) randomize the teams
   2) prevent the higher-tier players get their best roles all the time
3. Assign players to the remaining roles one-by-one.
   For each iteration, a player is assigned to the team whose total tier score is less than the other team.
   If a role has already been assigned to the team, skip the player. The skipped player may be assigned to the other team.
"""
import csv
import random
import sys
from typing import List, Tuple

from constants import *
from players import *


class Team:
    def __init__(self):
        # {role: PlayerRole}
        self.squad = {}

        # Tier sum of this team
        self.tier_sum = 0

    def __str__(self):
        return "\n".join([str(self.squad.get(role)) for role in ALL_ROLES])

    def __repr__(self):
        return self.__str__()

    def add(self, player_role: PlayerRole):
        self.squad[player_role.role] = player_role
        self.tier_sum += player_role.tier


def make_teams(player_roles: List[PlayerRole]) -> Tuple[Team, Team]:
    # 0. assert and init
    players = set([p.name for p in player_roles])
    assert len(players) == 10

    team_a = Team()
    team_b = Team()
    assigned_players = set()

    # 1. Sort player_roles by tier
    sorted_player_roles = sorted(player_roles, key=lambda p: p.tier, reverse=True)

    # 2. Randomly assign one player to each team
    player_role = random.choice(sorted_player_roles)
    team_a.add(player_role)
    assigned_players.add(player_role.name)
    while True:
        player_role = random.choice(sorted_player_roles)
        if player_role.name not in assigned_players:
            team_b.add(player_role)
            assigned_players.add(player_role.name)
            break

    # 3. Assign players to the remaining roles one-by-one.
    i_a = 0
    i_b = 0
    while i_a < len(sorted_player_roles) and i_b < len(sorted_player_roles):
        # For each iteration, a weaker team selects a player.
        if team_a.tier_sum < team_b.tier_sum:
            i_a = select_player(team_a, sorted_player_roles, i_a, assigned_players)
        else:
            i_b = select_player(team_b, sorted_player_roles, i_b, assigned_players)

    return team_a, team_b


def select_player(team: Team, sorted_player_roles: List[PlayerRole], i: int, assigned_players: List[str]) -> int:
    """
    Select a player for the team.

    Args:
        team: The team to select a player.
        sorted_player_roles: The player pool sorted by the tier of player's role in descending order.
        i: The index of the player pool to be selected for the team.
        assigned_players: The list of players that have already been assigned to a team.

    Returns:
        The index of the next player to be selected for the team.
    """
    if len(team.squad) == len(ALL_ROLES):
        return len(sorted_player_roles)

    # If the player is already assigned to any team or the team already took the role, skip to next player.
    while i < len(sorted_player_roles):
        player_role = sorted_player_roles[i]
        i += 1

        if player_role.name not in assigned_players and player_role.role not in team.squad:
            team.add(player_role)
            assigned_players.add(player_role.name)
            break

    return i


if __name__ == "__main__":
    player_names = sys.argv[1:]

    player_roles = []
    for name in player_names:
        with open(f"data/{name}.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                player_roles.append(PlayerRole(row["player"], row["role"], int(row["tier"])))

    team_a, team_b = make_teams(player_roles)

    print(f"Team A (Total tier = {team_a.tier_sum})")
    print(team_a)
    print()
    print(f"Team B (Total tier = {team_b.tier_sum})")
    print(team_b)
