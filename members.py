# -*- coding: utf-8 -*-
"""
Class for the members of the garden club

@author: Mark
"""
from dataclasses import dataclass
import pickle
from typing import List
from configuration import MEMBERFILE, SAVEDMEMBERS


@dataclass
class Member:
    """ Current member of Garden Club """
    first_name: str
    last_name: str

    def __repr__(self) -> str:
        return f'{self.first_name} {self.last_name}'


def load_members_from_file() -> List[Member]:
    """ Initial load of members from file """
    members: List[Member] = []
    with open(MEMBERFILE, encoding="UTF-8") as data:
        for line in data:
            name = line.split()
            members.append(Member(*name))
    return members


def save_members(members: List[Member]) -> None:
    """ Back up members to disk """
    with open(SAVEDMEMBERS, 'wb') as save_file:
        pickle.dump(members, save_file)


def load_members() -> List[Member]:
    """ Load schedule from disk """
    with open(SAVEDMEMBERS, 'rb') as read_file:
        return pickle.load(read_file)


def main() -> None:
    """ Runs only as tests """
    members = load_members_from_file()
    save_members(members)
    members = load_members()
    print(members)


if __name__ == '__main__':
    main()
