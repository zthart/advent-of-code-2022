#! /usr/bin/python3
# -*- coding: utf-8 -*-

from os import path
from enum import Enum

MarkerLengths = Enum("MarkerLengths", [("PACKET", 4), ("MESSAGE", 14)])


def main(marker_length=MarkerLengths.PACKET):
    counted = 0
    buff = ""
    seen_map = {}
    with open(path.join(path.dirname(__file__), "input.txt"), "r") as in_file:
        while char := in_file.read(1):
            counted += 1
            if len(buff) == marker_length.value:
                removed = buff[0]
                buff = buff[1:]
                seen_map[removed] -= 1
                if seen_map[removed] == 0:
                    del seen_map[removed]
            buff += char
            if char in seen_map:
                seen_map[char] += 1
            else:
                seen_map[char] = 1

            if len(seen_map) == marker_length.value:
                break

    return counted


if __name__ == "__main__":
    counted = main()
    message_counted = main(MarkerLengths.MESSAGE)
    print(
        f"Total chars counted until start-of-packet:\t{counted}\n"
        f"Total chars counted until start-of-message:\t{message_counted}"
    )
