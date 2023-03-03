# -*- coding: utf-8 -*-
"""
Module to hold data about awards made for show entries.

@author: Mark
"""
from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from garden_show.Show import Section, ShowClass
from typing import List
from strenum import StrEnum


class AwardType(StrEnum):
    BEST = "Best in "
    POINTS = "Most points in "


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
class Group:
    """The group of sections or show classes
    for which a particular award is made."""

    with_members: List[Section | ShowClass]
