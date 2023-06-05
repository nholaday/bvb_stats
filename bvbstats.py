import argparse
from pathlib import Path
from pprint import pprint

# Example
# R fs A 2 3 hdl N k
# Reilly serve Andrew 2 pass rating 3 set rating hard driven line at Nic for kill


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    return args


def init_data(players):
    stats = {}
    for player in players:
        stats.update(
            {
                player: {
                    "serve": [],
                    "pass": [],
                    "attack": [],
                    "set": [],
                    "dig": [],
                    "block": [],
                    "sideout": [],
                },
            }
        )
    return stats


def update_stats(stats, player, score, action):
    """Modify the stats dictionary depending on the actions"""
    if action == "fs" or action == "jfs" or action == "ts" or action == "jts":  # float serve
        stats[player]["serve"].append(score)
    elif action == "p":  # pass/serve receive
        stats[player]["pass"].append(score)
    elif action == "s":  # set
        stats[player]["set"].append(score)
    elif action == "hdl" or action == "hda":  # hard driven line, hard driven angle
        stats[player]["attack"].append(score)
    elif action == "sl" or action == "sa":  # shoot line, shoot angle
        stats[player]["attack"].append(score)
    elif action == "d":  # dig
        stats[player]["dig"].append(score)
    elif action == "b":  # block
        stats[player]["block"].append(score)
    # TODO: change to match case statement new to python 3.10


def intepret_line(stats, commands):
    """Interpret the player, score, and actions of the line"""
    i = 0
    while i < len(commands):
        # commands alternate between the player and the score+action
        player = commands[i]
        # TODO: interpret with regex instead of just pulling out first character to account for "-1" or "0.5"
        score = commands[i + 1][0]
        action = commands[i + 1][1:]
        update_stats(stats, player, score, action)

        i += 2
    # TODO: automatically interpret player based on context. For example,
    # if there's a set after a pass we know it's the player's partner
    # TODO: automatically interpret score based on context. For example,
    # if a player scores 3p (in system pass), the serve would always have a score of 1
    # could do it by seeing an action then crawling nearby actions by moving the index
    # to find the needed info
    # TODO: record the score of the game


def main():
    players = ["T", "N", "A", "S"]
    stats = init_data(players)

    args = get_args()
    filename = Path(args.path)
    with open(filename, "r") as file:
        for line in file:
            print(line)
            commands = line.split(" ")
            intepret_line(stats, commands)

    pprint(stats)
    # TODO: calculate stats based on raw data
    # TODO: intepret on 2 stats


if __name__ == "__main__":
    main()
