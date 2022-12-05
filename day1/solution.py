#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os
import heapq
import functools


class ElfSnacks:
    def __init__(self):
        self._heap = []

    def add_elf_cals(self, cals):
        heapq.heappush(self._heap, cals)

    def get_top_cals(self):
        return self.get_sum_of_top_n(1)

    def get_sum_of_top_n(self, n):
        return functools.reduce(
            lambda acc, n: acc + n, heapq.nlargest(n, self._heap)
        )


def main():
    snacks = ElfSnacks()
    running_total = 0
    with open(
        os.path.join(os.path.dirname(__file__), "input.txt"), "r"
    ) as in_file:
        for line in in_file:
            if (cals := line.rstrip()) != "":
                running_total += int(cals)
            else:
                snacks.add_elf_cals(running_total)
                running_total = 0

    return snacks


if __name__ == "__main__":
    all_snacks = main()
    print(
        f"top:\t{all_snacks.get_top_cals()}\n"
        f"top 3:\t{all_snacks.get_sum_of_top_n(3)}"
    )
