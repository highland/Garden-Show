# -*- coding: utf-8 -*-
"""
Module to hold data about awards made for show entries.

@author: Mark
"""
from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from typing import List, Tuple
from pathlib import Path

import tomli
from strenum import StrEnum

# from garden_show.Show import schedule
from garden_show.configuration import AWARDFILE, AWARDDATA


Description = str
TrophyName = str

ClassId = str  # r'\D\d*'
SectionId = str  # r"\D"
ExhibitorName = str
Bests = List[Tuple[Description, List[ClassId | SectionId], TrophyName]]


class AwardType(StrEnum):
    """An enumeration of the types of Award"""

    BEST = "best"
    POINTS = "points"


class GroupType(StrEnum):
    """An enumeration of the targets of an Award"""

    SECTIONS = "section"
    CLASSES = "show_class"


class WinsType(StrEnum):
    """An enumeration of what the Award wins"""

    TROPHY = "trophy"
    ROSETTE = "rosette"


@dataclass
class Award:
    """Class for all the different types of awards
    (trophies, rosettes, etc.)."""

    wins: WinsType
    type: AwardType
    with_members: List[ClassId | SectionId]
    group_type: GroupType
    name: str
    description: str = ""
    winner: List[ExhibitorName] = field(default_factory=list)


@dataclass
class Trophy(Award):
    """class for a trophy award"""

    title: str = ""


@dataclass
class Rosette(Award):
    """class for a rosette award"""


def _load_award_structure_from_file(file: Path = AWARDFILE) -> List[Award]:
    """Initial load of award structure from
    TOML file"""
    with file.open("rb") as structure_file:
        award_structure = tomli.load(structure_file)
        award_list = []
        for award_type, data in award_structure["trophies"].items():
            wins = WinsType.TROPHY
            for award in data:
                group_type = (
                    GroupType.SECTIONS
                    if award.get("section")
                    else GroupType.CLASSES
                    if award.get("show_class")
                    else None
                )
                award_type = AwardType(award_type)
                with_members = (
                    award.get("section")
                    if group_type == GroupType.SECTIONS
                    else award.get("show_class")
                    if group_type == GroupType.CLASSES
                    else None
                )
                award = Award(
                    wins,
                    award_type,
                    with_members,
                    group_type,
                    award.get("name"),
                    award.get("description"),
                )
                award_list.append(award)
    return award_list


def save_awards() -> None:
    """Back up awards to disk"""
    with AWARDDATA.open("wb") as save_file:
        pickle.dump(awards, save_file)


def _load_awards() -> List[Award]:
    """Load awards from disk"""
    #    if not AWARDDATA.exists():  # not yet loaded from file
    return _load_award_structure_from_file()


awards: List[Award] = _load_awards()


def bests_for_section(section_id: str) -> Bests:
    """Used to construct the 'best in ...' input fields for a section"""
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
