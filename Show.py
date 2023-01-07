# -*- coding: utf-8 -*-
"""
Module to load and hold all show data

@author: Mark
"""
from schedule import Schedule, load_schedule, save_schedule
from exhibitors import Exhibitor, load_exhibitors, save_exhibitors
from typing import List

schedule: Schedule = load_schedule()
exhibitors: List[Exhibitor] = load_exhibitors()


def save_show_data():
    save_schedule(schedule)
    save_exhibitors(exhibitors)
