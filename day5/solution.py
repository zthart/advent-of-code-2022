#! /usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Optional
from os import path


class Crate:
    """Represents a single crate, it's contents, and points to the crate beneath, if any
    """

    def __init__(self, contents: str):
        self._contents = contents
        self._beneath = None

    @property
    def contents(self) -> str:
        """The read-only contents of this crate"""
        return self._contents

    @property
    def beneath(self) -> Crate:
        """Pointer to the create beneath `self`"""
        return self._beneath

    @beneath.setter
    def beneath(self, other: Crate):
        self._beneath = other

    @beneath.deleter
    def beneath(self):
        self._beneath = None


class Stack:
    """LIFO Stack of Crates"""

    def __init__(self):
        self._top = None

    def peek(self) -> Optional[Crate]:
        """Return the crate at the top of the stack, without removing it"""
        return self._top

    def push(self, crate: Crate):
        """Push a crate onto the stack"""
        crate.beneath = self._top
        self._top = crate

    def pop(self) -> Optional[Crate]:
        """Pop a crate off of the stack"""
        if crate := self._top:
            self._top = crate.beneath
            del crate.beneath
            return crate
        return None

    def move_one_to_other(self, other: Stack):
        """Moves one crate from the top of this stack to the top of `other`"""
        other.push(self.pop())

    def move_n_to_other(self, n: int, other: Stack):
        """Moves n crates from the top of this stack to the top of `other`, one at a time
        """
        for _ in range(n):
            self.move_one_to_other(other)

    def move_all_n_to_other(self, n, other: Stack):
        substack = Stack()  # hold our "stack" of items being moved here
        for _ in range(n):
            substack.push(self.pop())

        while crate := substack.pop():
            other.push(crate)
        pass


def build_stacks(rows):
    # remove the last row, since it's the col indices, figure out how many stacks
    stacks = [None] * int(rows.pop().strip().split("   ")[-1])
    # iterate in reverse, building our stacks from the bottom up
    for row in rows[::-1]:
        idx = 0
        while idx < len(row):
            curr_stack_idx = idx // 4

            if (contents := row[idx + 1 : idx + 2]) != " ":
                crate = Crate(contents)
                if stack := stacks[curr_stack_idx]:
                    stack.push(crate)
                else:
                    stack = Stack()
                    stack.push(crate)
                    stacks[curr_stack_idx] = stack

            idx += 4

    return stacks


def main(advanced_cranes=False):
    # will convert these to an array of Stacks once we've read in the input fully
    stack_rows = []
    stacks = None
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as in_file:
        while (line := in_file.readline()) != "\n":
            # we're not stripping the newline here because it means all our rows
            # have a length that is evenly divisible by 4
            stack_rows.append(line)

        stacks = build_stacks(stack_rows)

        while line := in_file.readline().strip():
            n, src, dest = [
                x if idx == 0 else x - 1
                for idx, x in enumerate([int(x) for x in line.split(" ")[1::2]])
            ]
            if advanced_cranes:
                stacks[src].move_all_n_to_other(n, stacks[dest])
            else:
                stacks[src].move_n_to_other(n, stacks[dest])

    return stacks


if __name__ == "__main__":
    stacks = main(advanced_cranes=True)
    contents = "".join([x.peek().contents for x in stacks])
    print(f"Top of stacks: {contents}")
