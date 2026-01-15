from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="main",
        screen_type="external",
        label="Main",
    ),
    DrawerScreen(
        value="question_mark",
        screen_type="internal",
        label="Question Mark",
    ),
]

ypiqs_drawer_app = DrawerApp(
    value="ypiqs",
    label="YPIQS",
    screens={screen.value: screen for screen in _screens},
)
