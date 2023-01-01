# -*- coding: utf-8 -*-
"""
Class representing a Façade for the GUI to access model data

@author: Mark
"""

from schedule import load_schedule, Schedule, Section, ShowClass
from exhibitors import load_exhibitors, Exhibitor
from entries import load_entries, Entry
from typing import List, Dict


_schedule = load_schedule()
if not (_exhibitors := load_exhibitors()):
    _exhibitors: List[Exhibitor] = []
if not (_entries := load_entries()):
    _exhibitor_entries: Dict[Exhibitor, Entry] = {}
    _class_entries: Dict[ShowClass, Entry] = {}
else:
    _exhibitor_entries, _class_entries = _entries


def exhibitor_check(exhibitor: Exhibitor) -> bool:
    return exhibitor in _exhibitors
