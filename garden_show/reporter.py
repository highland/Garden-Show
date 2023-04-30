# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 14:57:37 2023

@author: Mark
"""

from enum import Enum
from garden_show import Show
import flet as ft


class Style(Enum):
    """An enumeration of the styles for output"""

    BODY = ft.TextThemeStyle.BODY_MEDIUM
    TITLE = ft.TextThemeStyle.TITLE_LARGE
    HEADING = ft.TextThemeStyle.TITLE_MEDIUM
    BIGBODY = ft.TextThemeStyle.BODY_LARGE


class Output(ft.ListView):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)
        self.auto_scroll = True
        self.height = 600

    def print(
        self, text: str, indent: int = 0, style: Style = Style.BODY
    ) -> None:
        self.controls.append(
            ft.Text(
                text,
                style=style.value,
                offset=ft.transform.Offset(0.02 * indent, 0),
            )
        )

    def clear(self) -> None:
        self.controls = []

    def divider(self) -> None:
        self.controls.append(ft.Divider())


def main(page: ft.Page):
    def show_results(event: ft.ControlEvent) -> None:
        output.clear()
        output.print("Results by Exhibitor", style=Style.TITLE)
        output.divider()
        awards = Show.awards.get_all_awards()
        for exhibitor in Show.exhibitors:
            if exhibitor.results:
                output.print(
                    f"Exhibitor {exhibitor}", style=Style.HEADING, indent=1
                )
                for result in exhibitor.results:
                    output.print(
                        f"{result.place.value}{result.show_class.class_id}",
                        indent=2,
                    )

            for award in awards:
                if award.winner == exhibitor.full_name:
                    if award.wins is Show.awards.WinsType.TROPHY:
                        output.print(
                            f"Winner of {award.name}:",
                            style=Style.BIGBODY,
                            indent=2,
                        )

                        output.print(
                            f"{award.description} "
                            f"{f'for {award.reason}' if award.reason else ''}",
                            style=Style.BODY,
                            indent=4,
                        )

                    elif award.wins is Show.awards.WinsType.ROSETTE:
                        output.print(
                            f"Awarded a Rosette for {award.description}",
                            style=ft.TextThemeStyle.BODY_LARGE,
                            indent=2,
                        )

        event.page.update()

    button_list = ft.Column()
    winners_btn = ft.ElevatedButton(
        "Results by Exhibitor", on_click=show_results
    )

    button_list.controls.append(winners_btn)
    output = Output()
    page.add(button_list)
    page.add(output)


ft.app(target=main)
