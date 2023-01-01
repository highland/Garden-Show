# -*- coding: utf-8 -*-
"""
Class for an entry in the Show by a member of the garden club

@author: Mark
"""
from dataclasses import dataclass
import pickle
from typing import Dict, Tuple, Literal
from schedule import ShowClass
from exhibitors import Exhibitor
from configuration import SAVEDENTRIES


@dataclass
class Entry:
    """ Current member of Garden Club """
    member: Exhibitor
    _class: ShowClass
    count: Literal[1, 2] = 1

    def __repr__(self) -> str:
        return f'{self.member}\t {self._class}'


def save_entries(exhibitor_entries: Dict[Exhibitor, Entry],
                 class_entries: Dict[ShowClass, Entry]) -> None:
    """ Back up entries to disk """
    with open(SAVEDENTRIES, 'wb') as save_file:
        pickle.dump(exhibitor_entries, save_file)
        pickle.dump(class_entries, save_file)


def load_entries() -> Tuple[Dict[Exhibitor, Entry], Dict[ShowClass, Entry]]:
    """ Load schedule from disk """
    with open(SAVEDENTRIES, 'rb') as read_file:
        return pickle.load(read_file)


def main() -> None:
    """ Runs only as tests """
    exhibitor_entries: Dict[Exhibitor, Entry] = {}
    class_entries: Dict[ShowClass, Entry] = {}

#   exhibitor_entries, class_entries = load_entries_from_file()
#    save_entries(exhibitor_entries, class_entries)
#    exhibitor_entries, class_entries = load_entries()
    print(exhibitor_entries, class_entries)


if __name__ == '__main__':
    main()
