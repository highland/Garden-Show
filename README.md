# Garden Show
 Application to support a garden club annual show

 Originally done with VBA in an Excel spreadsheet.
 This had become unmanageable over the years as changes accumulated.

 The replacement project will be written in python with a simple frontend.
 Uses flet for GUI, pickle for data persistence*,
 xlsxwriter for report generation as Excel spreadsheets,
 and batch input of the schedule from a text file. The awards to be presented
 in the show are defined in a .toml file.

 Intended for use by Badenoch Gardening Club, it should however be suitable
 for any Gardening Club that runs a traditional Garden Show

(*) A spike to try out ZODB instead of straight pickle came to the
conclusion that ZODB was overkill for this application.

Uses python 3.11.3
