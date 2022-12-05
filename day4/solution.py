#! /usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from os import path
from itertools import starmap


class Range:
    """Represents a section of the elf camp, ends of the range are **inclusive**
    """

    def __init__(self, start: int, end: int) -> Range:
        self.start = start
        self.end = end
        self.width = end - start

    def overlaps(self, other: Range) -> bool:
        """Return true if this range overlaps with other"""

        return (
            other.start >= self.start
            and other.start <= self.end
            or self.start >= other.start
            and self.start <= other.end
        )

    def subset_of(self, other: Range) -> bool:
        """Return true if this range is a strict subset of other

        This is not a bidirectional comparison, if the `other` range is a
        subset of this, this function will still return `False`
        """
        if other.width < self.width:
            return False

        return self.start >= other.start and self.end <= other.end


def main():
    subset_total = 0
    overlap_total = 0
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as in_file:
        for line in in_file:
            range_1, range_2 = list(
                starmap(  # starmap the two range values into proper Range instances
                    Range,
                    [
                        # Turn the parsed strings below into sub-arrays of
                        # integers like [[a, b], [x, y]]
                        list(map(int, l.split("-")))
                        # strip each line, split on the comma to get two
                        # ranges of the form ["A-B", "X-Y"]
                        for l in line.strip().split(",")
                    ],
                )
            )
            if range_1.subset_of(range_2) or range_2.subset_of(range_1):
                subset_total += 1
            if range_1.overlaps(range_2):
                overlap_total += 1

    return (subset_total, overlap_total)


if __name__ == "__main__":
    subset_total, overlap_total = main()
    print(
        f"Total subset pairs:\t{subset_total}\n"
        f"Overlapping pairs:\t{overlap_total}"
    )
