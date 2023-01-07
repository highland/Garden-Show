# -*- coding: utf-8 -*-
"""
Class for the exhibitors at the garden show

@author: Mark
"""
import os
from dataclasses import dataclass, field
import pickle
from typing import List
from configuration import SAVEDEXHIBITORS
from entries import Entry


@dataclass
class Exhibitor:
    """Current member of Garden Club"""

    first_name: str
    last_name: str
    member: bool = True
    entries: List[Entry] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other: "Exhibitor") -> bool:
        return (
            self.first_name == other.first_name
            and self.last_name == other.last_name
        )

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name))


def save_exhibitors(exhibitors: List[Exhibitor]) -> None:
    """Back up exhibitors to disk"""
    with open(SAVEDEXHIBITORS, "wb") as save_file:
        pickle.dump(exhibitors, save_file)


def load_exhibitors() -> List[Exhibitor]:
    """Load schedule from disk
    return empty list if file does not exist"""
    with open(SAVEDEXHIBITORS, "rb") as read_file:
        return pickle.load(read_file)
    if not os.path.exists(SAVEDEXHIBITORS):  # not yet loaded from file
        return []
    else:
        with open(SAVEDEXHIBITORS, "rb") as read_file:
            return pickle.load(read_file)
