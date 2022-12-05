#! /usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from os import path


ASCII_UPPER_A = 65
ASCII_LOWER_A = 97
GROUP_SIZE = 3


class ElfGroup:
    def __init__(self, *rucksacks) -> ElfGroup:
        self.rucksacks = rucksacks

    def get_badge_type(self) -> str:
        """Return the single common item between all rucksacks in the group"""
        sets = list(
            map(lambda s: {i for i in s.get_contents()}, self.rucksacks)
        )
        intersection = sets[0].intersection(*sets[1:])
        assert len(intersection) == 1
        return intersection.pop()


class Rucksack:
    def __init__(self, contents: str) -> Rucksack:
        self.compartments = [
            # Split the compartments up
            contents[: len(contents) // 2],
            contents[len(contents) // 2 :],
        ]

    def get_contents(self) -> str:
        """Return the full contents of the rucksack"""
        return "".join(self.compartments)

    def get_common_item(self) -> str:
        """Return the common item between the two compartments of the rucksack

        This may not be the most efficient way to do it, but it sure is easy to understand
        """
        set_a = {i for i in self.compartments[0]}
        set_b = {j for j in self.compartments[1]}
        intersection = set_a.intersection(set_b)
        assert len(intersection) == 1
        return intersection.pop()

    @staticmethod
    def get_item_priority(item: str) -> int:
        """Return the integer priority of a given item"""
        if ord(item) <= ASCII_LOWER_A:  # ascii uppercase
            return ord(item) - ASCII_UPPER_A + 27
        return ord(item) - ASCII_LOWER_A + 1  # all priorities > 0


def main():
    running_total = 0
    badge_total = 0
    curr_group = []
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as in_file:
        for line in in_file:
            curr_rucksack = Rucksack(line.strip())
            common_item = curr_rucksack.get_common_item()
            running_total += Rucksack.get_item_priority(common_item)
            curr_group.append(curr_rucksack)

            if len(curr_group) == GROUP_SIZE:
                group = ElfGroup(*curr_group)
                badge_type = group.get_badge_type()
                badge_total += Rucksack.get_item_priority(badge_type)
                curr_group = []

    return (running_total, badge_total)


if __name__ == "__main__":
    (total, badge_total) = main()
    print(f"Total priority:\t{total}\nBadge priority:\t{badge_total}")
