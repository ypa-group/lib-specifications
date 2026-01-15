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
        value="categories",
        screen_type="external",
        label="Categories",
    ),
    DrawerScreen(
        value="disable_btn",
        screen_type="external",
        label="Disable Button",
    ),
    DrawerScreen(
        value="demo",
        screen_type="external",
        label="Demo",
    ),
]

budget_drawer_app = DrawerApp(
    value="budget",
    label="Budget",
    screens={screen.value: screen for screen in _screens},
)
