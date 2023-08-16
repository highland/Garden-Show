# -*- coding: utf-8 -*-
"""
Locations of data files and Constants

@author: Mark
"""
from pathlib import Path

TITLE: str = "Badenoch Gardening Club"

_ROOT: Path = Path("D:/BGC Show/Garden-Show/Data")
assert _ROOT.exists()

SCHEDULEFILE: Path = _ROOT / "schedule.txt"
NAMESFILE: Path = _ROOT / "names.txt"
SAVEDDATA: Path = _ROOT / "data.pkl"
AWARDFILE: Path = _ROOT / "awards.toml"
AWARDDATA: Path = _ROOT / "awards.pkl"
IMAGEFILE: Path = _ROOT / "Graphic.png"
JUDGESSHEETS: Path = _ROOT / "JudgesSheets.xlsx"

EXCEL: str = "C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE"
