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
        value="constructor",
        screen_type="external",
        label="Constructor",
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


calculator_drawer_app = DrawerApp(
    value="calculator",
    label="Calculator",
    screens={screen.value: screen for screen in _screens},
)
