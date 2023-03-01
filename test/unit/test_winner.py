#!/usr/bin/env python

import unittest
from garden_show import Show


class TestWinner(unittest.TestCase):
    def setUp(self) -> None:
        self.testclass = Show.schedule.classes["A1"]
        self.winnername = "Mark Thomas"
        # take backup
        self.old_exhibitors = Show.exhibitors[:]
        # clear out
        Show.exhibitors = []

    def tearDown(self) -> None:
        # restore
        Show.exhibitors = self.old_exhibitors
        self.testclass.remove_results()

    def test_post_init(self) -> None:
        self.testexhibitor = Show.get_actual_exhibitor(self.winnername)
        testwinner = Show.Winner(self.testexhibitor, self.testclass, "1st", 3)

        self.assertIn(
            testwinner,
            self.testexhibitor.results,
            "Link from Exhibitor to Winner not created",
        )
        self.assertIn(
            testwinner,
            self.testclass.results,
            "Link from ShowClass to Winner not created",
        )

    def test_get_actual_exhibitor(self) -> None:
        exhibitor_name = "Attila the Hun"
        first, *other, last = exhibitor_name
        missing_person = Show.Exhibitor(first, last, other)
        self.assertNotIn(
            missing_person,
            Show.exhibitors,
            "Failed to empty exhibitors for test",
        )
        new_person = Show.get_actual_exhibitor(self.winnername)
        self.assertIn(
            new_person,
            Show.exhibitors,
            "Missing Exhibitor not added to exhibitors",
        )
