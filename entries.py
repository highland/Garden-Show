# -*- coding: utf-8 -*-
"""
Class for an entry in the Show by a member of the garden club

@author: Mark
"""
from dataclasses import dataclass
import pickle
from typing import Dict, Tuple
from schedule import SubSection
from members import Member
from configuration import SAVEDENTRIES


@dataclass
class Entry:
    """ Current member of Garden Club """
    member: Member
    _class: SubSection

    def __repr__(self) -> str:
        return f'{self.member}\t {self._class}'


# def load_entries_from_file() -> Tuple[Dict[Member, Entry],
#                                       Dict[SubSection, Entry]]:
#     """ Initial load of members from file """
#     members: List[Member] = []
#     with open(MEMBERFILE, encoding="UTF-8") as data:
#         for line in data:
#             name = line.split()
#             members.append(Member(*name))
#     return members


def save_entries(member_entries: Dict[Member, Entry],
                 class_entries: Dict[SubSection, Entry]) -> None:
    """ Back up entries to disk """
    with open(SAVEDENTRIES, 'wb') as save_file:
        pickle.dump(member_entries, save_file)
        pickle.dump(class_entries, save_file)


def load_entries() -> Tuple[Dict[Member, Entry], Dict[SubSection, Entry]]:
    """ Load schedule from disk """
    with open(SAVEDENTRIES, 'rb') as read_file:
        return pickle.load(read_file)


def main() -> None:
    """ Runs only as tests """
    member_entries: Dict[Member, Entry] = {}
    class_entries: Dict[SubSection, Entry] = {}

#    member_entries, class_entries = load_entries_from_file()
    save_entries(member_entries, class_entries)
    member_entries, class_entries = load_entries()
    print(member_entries, class_entries)


if __name__ == '__main__':
    main()
