# -*- coding: utf-8 -*-
"""
Module to hold data about awards made for show entries.

@author: Mark
"""
from __future__ import annotations

import pickle
from abc import ABC
from dataclasses import dataclass
from typing import List, Optional, Callable, Tuple

import tomli
from strenum import StrEnum

from garden_show.Show import Section, ShowClass, Exhibitor
from garden_show.configuration import AWARDFILE, AWARDDATA


Description = str
Class_or_Section_id = str
Trophy_name = str

Bests = List[Tuple[Description, List[Class_or_Section_id], Trophy_name]]


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
    winner: Optional[Exhibitor] = None
    _determine_winner: Optional[Callable] = None


@dataclass
class Trophy(Award):
    """class for a trophy award"""

    title: str = ""


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


def determine_award_winners() -> None:
    global awards
    for award in awards:
        award._determine_winner()


def _load_award_structure_from_file(file: str = AWARDFILE) -> List[Award]:
    """Initial load of award structure from
    TOML file"""
    with open(file, "rb") as structure_file:
        award_structure = tomli.load(structure_file)
        award_list = []
        for award_type, data in award_structure["trophies"].items():
            for award in data:
                if groups := award.get("section"):
                    group_type = GroupType("section")
                elif groups := award.get("show_class"):
                    group_type = GroupType("show_class")
                group = Group(
                    groups, group_type, award.get("description", "")
                )
                award_type = AwardType(award_type)
                award_list.append(
                    Trophy(award_type, group, award.get("name"))
                )

    return award_list


def save_awards() -> None:
    """Back up awards to disk"""
    global awards
    with open(AWARDDATA, "wb") as save_file:
        pickle.dump(awards, save_file)


def _load_awards() -> List[Award]:
    """Load awards from disk"""
    #    if not os.path.exists(AWARDDATA):  # not yet loaded from file
    return _load_award_structure_from_file()


awards: List[Award] = _load_awards()


def bests_for_section(section_id: str) -> Bests:
    return [
        (
            award.in_group.description
            if award.in_group.group_type is GroupType.CLASSES
            else "Best in section",
            award.in_group.with_members,
            award.winner,
        )
        for award in awards
        if award.type is AwardType.BEST
        and award.in_group.with_members[0].startswith(section_id)
    ]
