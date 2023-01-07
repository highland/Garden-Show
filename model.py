# -*- coding: utf-8 -*-
"""
Class representing a Façade for the GUI to access data

Loads and holds all the application data.
Functions for the GUI all take and return only strings.

As the entries rely on a stable schedule,
    changes to the schedule should not take place
    once the first entry has been processed.

@author: Mark
"""
from typing import Optional, List
import Show


def exhibitor_check(name: str) -> Optional[List[str]]:
    """
    If the exhibitor exists, return their entries, else None.

    Args:
        name (str): Exhibitor name

    Returns:
        list of entries for this exhibitor or None

    """
    first, *_, last = name.split()
    test_exhibitor = Show.Exhibitor(first, last)
    if test_exhibitor in Show.exhibitors:
        return [
            str(entry) for entry in Show.get_actual_exhibitor(test_exhibitor)
        ]
    return None
