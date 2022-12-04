#! /usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from os import path
from enum import Enum
from abc import ABC, abstractmethod

Results = Enum("Results", [("LOSS", "X"), ("DRAW", "Y"), ("WIN", "Z")])
ResultScores = {Results.LOSS: 0, Results.DRAW: 3, Results.WIN: 6}


class Move(ABC):
    @abstractmethod
    def for_outcome(self, outcome: Results) -> Move:
        """Return the move to play given the desired outcome"""
        pass


class Rock(Move):
    def __init__(self):
        self.value = 1

    def for_outcome(self, outcome):
        if outcome == Results.DRAW:
            return Rock()
        if outcome == Results.LOSS:
            return Scissors()
        return Paper()


class Paper(Move):
    def __init__(self):
        self.value = 2

    def for_outcome(self, outcome):
        if outcome == Results.DRAW:
            return Paper()
        if outcome == Results.LOSS:
            return Rock()
        return Scissors()


class Scissors(Move):
    def __init__(self):
        self.value = 3

    def for_outcome(self, outcome):
        if outcome == Results.DRAW:
            return Scissors()
        if outcome == Results.LOSS:
            return Paper()
        return Rock()


MoveKey = {
    "A": Rock,
    "B": Paper,
    "C": Scissors,
}


class RPS:
    def __init__(self, them, us):
        self._them = MoveKey[them]()
        self._us_outcome = Results(us)

    def score(self):
        to_play = self._them.for_outcome(self._us_outcome)
        return to_play.value + ResultScores[self._us_outcome]


def main():
    running_total = 0
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as in_file:
        for line in in_file:
            curr_round = RPS(*line.strip().split(" "))
            running_total += curr_round.score()

    return running_total


if __name__ == "__main__":
    total = main()
    print(f"Total score:\t{total}")
