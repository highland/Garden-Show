# -*- coding: utf-8 -*-
"""
Module to hold data about awards made for show entries.

@author: Mark
"""
from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from garden_show.Show import Section, ShowClass
from garden_show.configuration import AWARDFILE, AWARDDATA
import pickle
import os
import tomli

from typing import List
from strenum import StrEnum


class AwardType(StrEnum):
    BEST = "best"
    POINTS = "points"


class GroupType(StrEnum):
    SECTIONS = "section"
    CLASSES = "show_class"


@dataclass
class Award(ABC):
    """Abstract superclass for different types of awards
    (trophies, rosettes, etc.)."""

    type: AwardType
    in_group: Group


@dataclass
class Trophy(Award):
    """class for a trophy award"""

    title: str


@dataclass
class Rosette(Award):
    """class for a rosette award"""


@dataclass
class Card(Award):
    """class for a card award"""


@dataclass
class Group:
    """The group of sections or show classes
    for which a particular award is made."""

    with_members: List[Section | ShowClass]
    group_type: GroupType
    description: str = ""


def _load_award_structure_from_file(file: str = AWARDFILE) -> List[Award]:
    """Initial load of award structure from TOML file"""
    with open(file, "rb") as structurefile:
        award_structure = tomli.load(structurefile)
        awards = []
        for awardtype, data in award_structure["trophies"].items():
            # TODO rosettes and cards
            if awardtype == AwardType.BEST:     # TODO points version
                for award in data:
                    if groups := award.get("section"):
                        group_type = GroupType("section")
                    elif groups := award.get("show_class"):
                        group_type = GroupType("show_class")
                    group = Group(groups, group_type,
                                  award.get("description", ""))
                    award_type = AwardType(awardtype)
                    awards.append(Trophy(award_type, group, award.get("name")))
    return awards


def save_awards(awards: List[Award]) -> None:
    """Back up awards to disk"""
    with open(AWARDDATA, "wb") as save_file:
        pickle.dump(awards, save_file)


def _load_awards() -> List[Award]:
    """Load awards from disk"""
    #    if not os.path.exists(AWARDDATA):  # not yet loaded from file
    return _load_award_structure_from_file()


awards: List[Award] = _load_awards()
