# -*- coding: utf-8 -*-
"""
Module to hold data about awards made for show entries.

@author: Mark
"""
from __future__ import annotations

import pickle
from dataclasses import dataclass
from typing import List
from pathlib import Path

import tomli
from strenum import StrEnum

from garden_show.configuration import AWARDFILE, AWARDDATA


ClassId = str  # r'\D\d*'
SectionId = str  # r"\D"
ExhibitorName = str


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
    winner: ExhibitorName = ""


def _load_award_structure_from_file(file: Path = AWARDFILE) -> List[Award]:
    """Initial load of award structure from
    TOML file"""
    with file.open("rb") as structure_file:
        award_structure = tomli.load(structure_file)
        award_list = []
        for award_type, data in award_structure["trophies"].items():
            for award_def in data:
                group_type = (
                    GroupType.SECTIONS
                    if award_def.get("section")
                    else GroupType.CLASSES
                    if award_def.get("show_class")
                    else None
                )
                with_members = (
                    award_def.get("section")
                    if group_type == GroupType.SECTIONS
                    else award_def.get("show_class")
                    if group_type == GroupType.CLASSES
                    else None
                )
                award = Award(
                    WinsType.TROPHY,
                    AwardType(award_type),
                    with_members,
                    group_type,
                    award_def.get("name"),
                    award_def.get("description", "Best in section"),
                )
                award_list.append(award)
    return award_list


def save_awards() -> None:
    """Back up awards to disk"""
    with AWARDDATA.open("wb") as save_file:
        pickle.dump(awards, save_file)


def _load_awards() -> List[Award]:
    """Load awards from disk"""
    if not AWARDDATA.exists():  # not yet loaded from file
        return _load_award_structure_from_file()

    with AWARDDATA.open("rb") as data_file:
        return pickle.load(data_file)


awards: List[Award] = _load_awards()


def bests_for_section(section_id: str) -> List[Award]:
    """Used to construct the 'best in ...' input fields for a section"""
    return [
        award
        for award in awards
        if award.type is AwardType.BEST
        and award.with_members[0].startswith(section_id)
    ]
