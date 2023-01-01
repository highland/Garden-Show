# -*- coding: utf-8 -*-
"""
Class for the exhibitors at the garden show

@author: Mark
"""
from dataclasses import dataclass
import pickle
from typing import List
from configuration import EXHIBITORFILE, SAVEDEXHIBITORS


@dataclass
class Exhibitor:
    """ Current member of Garden Club """
    first_name: str
    last_name: str
    member: bool = True

    def __repr__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __eq__(self, other: "Exhibitor") -> bool:
        return (self.first_name == other.first_name
                and self.last_name == other.last_name)


def load_exhibitors_from_file() -> List[Exhibitor]:
    """ Initial load of exhibitors from file """
    exhibitors: List[Exhibitor] = []
    with open(EXHIBITORFILE, encoding="UTF-8") as data:
        for line in data:
            name = line.split()
            exhibitors.append(Exhibitor(*name))
    return exhibitors


def save_exhibitors(exhibitors: List[Exhibitor]) -> None:
    """ Back up exhibitors to disk """
    with open(SAVEDEXHIBITORS, 'wb') as save_file:
        pickle.dump(exhibitors, save_file)


def load_exhibitors() -> List[Exhibitor]:
    """ Load schedule from disk """
    with open(SAVEDEXHIBITORS, 'rb') as read_file:
        return pickle.load(read_file)


# def main() -> None:
#     """ Runs only as tests """
#     exhibitors = load_exhibitors_from_file()
#     save_exhibitors(exhibitors)
#     exhibitors = load_exhibitors()
#     print(exhibitors)


# if __name__ == '__main__':
#     main()
