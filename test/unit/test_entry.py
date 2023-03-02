import unittest
from garden_show import Show


class TestEntry(unittest.TestCase):
    """The Entry class is responsible for connecting itself to
    the exhibitor on contruction.
    This is done by a __post_init__ method.
    In addition the Entry must ensure that it connects to the correct
    exhibitor instance.
    This is done using the get_actual_exhibitor function
    (tested in TestWinner)
    """

    def setUp(self) -> None:
        self.testclass = Show.schedule.classes["A1"]
        self.exhibitor_name = "Mark Thomas"
        # take backup
        self.old_exhibitors = Show.exhibitors[:]
        # clear out
        Show.exhibitors = []

    def tearDown(self) -> None:
        # restore
        Show.exhibitors = self.old_exhibitors

    def test_post_init(self) -> None:
        testexhibitor = Show.get_actual_exhibitor(self.exhibitor_name)
        testentry = Show.Entry(testexhibitor, self.testclass)

        self.assertIn(
            testentry,
            testexhibitor.entries,
            "Link from Exhibitor to Entry not created",
        )
