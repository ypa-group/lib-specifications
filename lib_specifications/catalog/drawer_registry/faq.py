from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="faq",
        screen_type="external",
        label="FAQ",
    ),
]

faq_drawer_app = DrawerApp(
    value="faq",
    label="FAQ",
    screens={screen.value: screen for screen in _screens},
)
