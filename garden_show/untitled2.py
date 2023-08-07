import flet
from garden_show.configuration import IMAGEFILE


def main(page: flet.Page):
    page.title = "Images Example"
    page.theme_mode = flet.ThemeMode.LIGHT
    page.padding = 50
    page.update()

    img = flet.Image(
        src=IMAGEFILE,
        fit=flet.ImageFit.CONTAIN,
    )

    entries = flet.TextButton(text="Entries Form")

    page.add(img)
    page.overlay.append(entries)
    page.update()



    # for i in range(0, 30):
    #     images.controls.append(
    #         flet.Image(
    #             src=f"https://picsum.photos/200/200?{i}",
    #             width=200,
    #             height=200,
    #             fit=flet.ImageFit.NONE,
    #             repeat=flet.ImageRepeat.NO_REPEAT,
    #             border_radius=flet.border_radius.all(10),
    #         )
    #     )
    # page.update()


flet.app(target=main)
