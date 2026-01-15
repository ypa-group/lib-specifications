from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="question_mark",
        screen_type="internal",
        label="Question Mark",
    ),
    DrawerScreen(
        value="main",
        screen_type="external",
        label="Main",
    ),
    DrawerScreen(
        value="demo",
        screen_type="external",
        label="Demo",
    ),
    DrawerScreen(
        value="decore",
        screen_type="external",
        label="Decore",
    ),
]

assistant_corporation_drawer_app = DrawerApp(
    value="assistant_corporation",
    label="Assistant Corporation",
    screens={screen.value: screen for screen in _screens},
)
