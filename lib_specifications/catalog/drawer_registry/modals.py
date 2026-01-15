from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="error",
        screen_type="internal",
        label="Error",
    ),
]

modals_drawer_app = DrawerApp(
    value="modals",
    label="Modals",
    screens={screen.value: screen for screen in _screens},
)
