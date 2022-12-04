#! /usr/bin/python3
# -*- coding: utf-8 -*-

from os import path
from enum import IntEnum

from abc import ABC, abstractmethod

Results = IntEnum("Results", [("LOSS", 0), ("DRAW", 3), ("WIN", 6)])


class Move(ABC):
    @abstractmethod
    def beats(self, other):
        pass


class Rock(Move):
    def __init__(self):
        self.value = 1

    def beats(self, other):
        if isinstance(other, Rock):
            return Results.DRAW
        if isinstance(other, Paper):
            return Results.LOSS
        return Results.WIN


class Paper(Move):
    def __init__(self):
        self.value = 2

    def beats(self, other):
        if isinstance(other, Paper):
            return Results.DRAW
        if isinstance(other, Scissors):
            return Results.LOSS
        return Results.WIN


class Scissors(Move):
    def __init__(self):
        self.value = 3

    def beats(self, other):
        if isinstance(other, Scissors):
            return Results.DRAW
        if isinstance(other, Rock):
            return Results.LOSS
        return Results.WIN


MoveKey = {
    "A": Rock,
    "B": Paper,
    "C": Scissors,
    "X": Rock,
    "Y": Paper,
    "Z": Scissors,
}


class RPS:
    def __init__(self, them, us):
        self._them = MoveKey[them]()
        self._us = MoveKey[us]()

    def score(self):
        return self._us.value + self._us.beats(self._them)


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
