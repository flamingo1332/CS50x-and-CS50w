# Simulate a sports tournament

import csv
import sys
import random
# import cs50

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")


    # TODO: Read teams into memory from file

    teams = []   # []는 list임
    filename = sys.argv[1]
    with open(filename)as file:
        reader = csv.DictReader(file)
        for team in reader:
            team["rating"] = int(team["rating"])
            teams.append(team)
        print(teams)

    # TODO: Simulate N tournaments and keep track of win counts

    counts = {}  # {}로 만들어진 list는 dictionary다. 승수 count하는데 사용됨
    for i in range(N):
        winner = simulate_tournament(teams)
        if winner in counts:
            counts[winner] += 1
        else:
            counts[winner] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []
    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # TODO
    while len(teams) > 1: #python의 len()은 string 대상으로는 글자수, list 나 tuple 대상으로는 항목 수를 결과로 돌려준다. dictionary는 모르겠다.
                            #여기서 teams 는 list기 때문에 list개수 구하는것.
        teams = simulate_round(teams)
    return teams[0]["team"]

if __name__ == "__main__":
    main()
