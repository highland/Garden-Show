import flet
import subprocess
from garden_show.configuration import IMAGEFILE, TITLE


def main(page: flet.Page):
    page.title = TITLE
    page.theme_mode = flet.ThemeMode.LIGHT
    page.padding = 20
    page.update()

    def add_exhibitors(e):
        subprocess.run("python addexhibitors.py", shell=True)

    def run_results_form(e):
        subprocess.run("python enterwinners.py")

    img = flet.Image(
        src=IMAGEFILE,
        width=1049,
        height=879,
        fit=flet.ImageFit.COVER,
    )

    actions = flet.Column(
        [
            flet.TextButton(text="Add Exhibitors", on_click=add_exhibitors),
            flet.TextButton(text="Results Form", on_click=run_results_form),
        ]
    )

    page.add(img)
    page.overlay.append(actions)
    page.update()


flet.app(target=main)
