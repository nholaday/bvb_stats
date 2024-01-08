import argparse
import re
from pathlib import Path
from pprint import pprint

# Example
# NsE2p3s1h

pass_to_serve_score = {"0": "4", "1": "2", "2": "1.5", "3": "1"}


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
    if (
        action == "fs" or action == "jfs" or action == "ts" or action == "jts"
    ):  # float serve
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


def intepret_serve(stats, partner, line):
    """Inteprets the stats for serve receive chunk"""
    # actions = re.search(r"([A-Z])(s)([A-Z])(-?\d)([p,h])(-?\d)([s,h])(-?\d)(h)", line)
    # TODO: score for attacking can be -1, account for 2 character score by
    # using regex or by moving an index instead of using an absolute index
    # could have a function that moves the index until it finds the action then interprets the
    # score behind it.

    # index that progresses through the line
    i = 0
    # Serve
    # 1st character is the server, then "s"
    # 3rd character is the receiver or "e" for service error or "a" for ace down the middle
    server = line[i]
    receiver = line[i + 2]
    if receiver == "e":
        stats[server]["serve"].append(0)
        return
    elif receiver == "a":
        stats[server]["serve"].append(4)
        return
    setter = partner[receiver]
    i += 3

    # Receive
    # 5th character is score for pass, then "p" OR
    # 5th character is score for attack(hit), then "h"
    if line[i + 1] == "p":
        stats[receiver]["pass"].append(line[i])
        stats[server]["serve"].append(pass_to_serve_score[line[i]])
    elif line[i + 1] == "h":
        stats[receiver]["attack"].append(line[i])
        stats[server].append(1)
        return
    elif line[i + 2] == "h":
        stats[receiver]["attack"].append(line[i : i + 2])
        stats[server].append(1)
        return
    i += 2

    # Set
    # 7th character is score for set, then "s" OR
    # 7th character is score for attack(hit) on 2, then "h"
    if line[i + 1] == "s":
        stats[setter]["set"].append(line[i])
        if line[i] == "0":
            return
    elif line[i + 1] == "h":
        stats[setter]["attack"].append(line[i])
        return
    elif line[i + 2] == "h":
        stats[setter]["attack"].append(line[i : i + 2])
        return
    i += 2

    # Attack
    # 8th character is score for attack, then "h"
    if line[i + 1] == "h":
        stats[receiver]["attack"].append(line[i])
    elif line[i + 1] == "h":
        stats[receiver]["attack"].append(line[i : i + 2])


def interpret_rally(stats, partner, line):
    """Interprets the stats for rally chunks"""
    i = 0
    # First character is the blocker or digger
    first_touch = line[i]
    i += 1

    # Block or dig(pass)
    if line[i + 1] == "p":
        stats[first_touch]["dig"].append(line[i])
    elif line[i + 1] == "b":
        stats[first_touch]["block"].append(line[i])
        if line[i] == "1":
            return
    elif line[i + 1] == "h":
        stats[first_touch]["attack"].append(line[i])
        return
    elif line[i + 2] == "h":
        stats[first_touch]["attack"].append(line[i : i + 2])
        return
    i += 2

    # Set
    # Ball can be set by either player in case of a block
    # Default to partner of blocker/digger unless specified
    sec_touch = partner[first_touch]

    if line[i + 1] == "s":
        stats[sec_touch]["set"].append(line[i])
    elif line[i + 1] == "h":
        stats[sec_touch]["attack"].append(line[i])
        return
    elif line[i + 2] == "s":
        sec_touch = line[i]
        stats[sec_touch]["set"].append(line[i + 1])
        i += 1
    elif line[i + 2] == "h":
        stats[sec_touch]["attack"].append(line[i : i + 2])
        return
    i += 2

    # Attack
    if line[i + 1] == "h":
        stats[sec_touch]["attack"].append(line[i])
    elif line[i + 2] == "h":
        stats[sec_touch]["attack"].append(line[i : i + 2])


def main():
    players = ["N", "J", "E", "F"]
    partner = {
        "N": "J",
        "J": "N",
        "E": "F",
        "F": "E",
    }
    stats = init_data(players)

    args = get_args()
    filename = Path(args.path)
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            # print(line, end="")
            if i == 0:
                title = line
                continue

            chunks = line.split(" ")
            for i, chunk in enumerate(chunks):
                try:
                    if i == 0:
                        intepret_serve(stats, partner, chunk)
                    else:
                        interpret_rally(stats, partner, chunk)
                except Exception as e:
                    print(f"Unable to parse {chunk} in {line}{e}")
            # pprint(stats)

    print(title)
    pprint(stats)
    # TODO: calculate stats based on raw data
    # TODO: intepret on 2 stats


if __name__ == "__main__":
    main()

# TODO: automatically interpret player based on context. For example,
# if there's a set after a pass we know it's the player's partner
# TODO: automatically interpret score based on context. For example,
# if a player scores 3p (in system pass), the serve would always have a score of 1
# could do it by seeing an action then crawling nearby actions by moving the index
# to find the needed info
# TODO: record the score of the game
# TODO: deal with overpasses/sets, they're not attacks but they're not errors
