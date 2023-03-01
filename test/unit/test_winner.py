#!/usr/bin/env python

from garden_show import Show

testclass = Show.schedule.classes["A1"]
winnername = "Mark Thomas"
testexhibitor = Show.get_actual_exhibitor(winnername)
testwinner = Show.Winner(testexhibitor, testclass, "1st", 3)
testwinner in testexhibitor.results
testwinner in testclass.results
testexhibitor in Show.exhibitors
