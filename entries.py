# -*- coding: utf-8 -*-
"""
Class for an entry in the Show by a member of the garden club

@author: Mark
"""
from collections import defaultdict
from dataclasses import dataclass
import pickle
from typing import Dict, Tuple, Literal, List
from schedule import ShowClass
from exhibitors import Exhibitor
from configuration import SAVEDENTRIES


@dataclass
class Entry:
    """Current member of Garden Club"""

    member: Exhibitor
    show_class: ShowClass
    count: Literal[1, 2] = 1

    def __repr__(self) -> str:
        return f"{self.member}\t {self.show_class}"


def save_entries(
    exhib_entries: Dict[Exhibitor, Entry], cls_entries: Dict[ShowClass, Entry]
) -> None:
    """Back up entries to disk"""
    with open(SAVEDENTRIES, "wb") as save_file:
        pickle.dump(exhib_entries, save_file)
        pickle.dump(cls_entries, save_file)


def load_entries() -> Tuple[Dict[Exhibitor, Entry], Dict[ShowClass, Entry]]:
    """Load schedule from disk"""
    try:
        with open(SAVEDENTRIES, "rb") as read_file:
            return pickle.load(read_file)
    except IOError:
        return defaultdict(list), defaultdict(list)


exhibitor_entries: Dict[Exhibitor, List[Entry]]
class_entries: Dict[ShowClass, List[Entry]]
exhibitor_entries, class_entries = load_entries()


def add_entries(exhibitor: Exhibitor, entries: List[Entry]) -> None:
    """
    Add the entries for a new exhibitor to the dicts
    for exhibitor_entries and class_entries.

    Args:
        exhibitor (Exhibitor): New exhibitor
        entries (List[ShowClass, int]): List of the classes entered,
        and how many of each (1 or 2).

    Returns:
        None

    """
    exhibitor_entries[exhibitor] = entries
    for entry in entries:
        class_entries[entry.show_class].append(entry)
    save_entries(exhibitor_entries, class_entries)


def delete_entries(exhibitor: Exhibitor) -> None:
    for entry in exhibitor_entries[exhibitor]:
        class_entries[entry.show_class].remove(entry)
    del exhibitor_entries[exhibitor]
    save_entries(exhibitor_entries, class_entries)


def get_exhibitor_entries(exhibitor) -> List[Entry]:
    return exhibitor_entries[exhibitor]


def getshow_class_entries(show_class: ShowClass) -> List[Entry]:
    return class_entries[show_class]


def main() -> None:
    """Runs only as tests"""

    #   exhibitor_entries, class_entries = load_entries_from_file()
    #    save_entries(exhibitor_entries, class_entries)
    #    exhibitor_entries, class_entries = load_entries()
    print(exhibitor_entries, class_entries)


if __name__ == "__main__":
    main()
