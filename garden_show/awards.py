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

from enum import StrEnum
import tomli

from garden_show.configuration import AWARDFILE, AWARDDATA


ClassId = str  # r'\D\d*'
SectionId = str  # r"\D"
ExhibitorName = str

awards: List[Award] = []


class AwardType(StrEnum):
    """An enumeration of the types of Award"""

    BEST = "best"
    POINTS = "points"
    POSITION = "position"


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
    reason: str = ""
    restriction: str = ""


def bests_for_section(section_id: SectionId) -> List[Award]:
    """Used to construct the 'best in ...' input fields for a section
    Note that if both Rosette and Trophy awards are included.
    only one field is required for both.
    """
    global awards
    if not awards:
        awards = get_all_awards()
    trophies = [
        award
        for award in awards
        if (award.type is AwardType.BEST and award.wins is WinsType.TROPHY)
        and (
            (
                len(award.with_members) == 1
                and award.with_members[0] == section_id
            )
            or (
                len(award.with_members) > 1
                and award.with_members[0].startswith(section_id)
            )
        )
    ]
    if trophies:
        bests = trophies
    else:
        bests = [
            award
            for award in awards
            if (
                award.type is AwardType.BEST
                and award.wins is WinsType.ROSETTE
                and award.with_members[0] == section_id
            )
        ]

    return bests


def _load_award_structure_from_file(file: Path = AWARDFILE) -> List[Award]:
    """Initial load of award structure from
    TOML file"""
    with file.open("rb") as structure_file:
        award_structure = tomli.load(structure_file)
        award_list = []

        for award_type, data in award_structure["trophies"].items():
            for award_def in data:
                if section_list := award_def.get("section"):
                    for section in section_list:
                        desc_default = (
                            "Best in section"
                            if AwardType(award_type) == AwardType.BEST
                            else "Most Points in section"
                        )
                        award = Award(
                            WinsType.TROPHY,
                            AwardType(award_type),
                            section,
                            GroupType.SECTIONS,
                            award_def.get("name"),
                            award_def.get("description", desc_default),
                        )
                        if restriction := award_def.get("restriction"):
                            award.restriction = restriction
                        award_list.append(award)
                if class_list := award_def.get("show_class"):
                    desc_default = (
                        "Best in class"
                        if AwardType(award_type) == AwardType.BEST
                        else "Most Points in class"
                        if AwardType(award_type) == AwardType.POINTS
                        else ""
                    )
                    award = Award(
                        WinsType.TROPHY,
                        AwardType(award_type),
                        class_list,
                        GroupType.CLASSES,
                        award_def.get("name"),
                        award_def.get("description", desc_default),
                    )
                    award_list.append(award)

        for award_type, data in award_structure["rosettes"].items():
            for award_def in data:
                with_members = award_def.get("section")
                for section in with_members:
                    description = (
                        "Best in section"
                        if AwardType(award_type) == AwardType.BEST
                        else "Most Points in section"
                        if AwardType(award_type) == AwardType.POINTS
                        else "First in section"
                    )
                    award = Award(
                        WinsType.ROSETTE,
                        AwardType(award_type),
                        section,
                        GroupType.SECTIONS,
                        "",
                        description,
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


def get_all_awards() -> List[Award]:
    """Allow other modules to access the awards data"""
    global awards
    if not awards:
        awards = _load_awards()
        save_awards()
    return awards


if __name__ == "__main__":
    awards = get_all_awards()
