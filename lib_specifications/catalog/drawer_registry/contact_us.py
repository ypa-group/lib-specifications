from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="idea",
        screen_type="external",
        label="Idea",
    ),
    DrawerScreen(
        value="review",
        screen_type="external",
        label="Review",
    ),
    DrawerScreen(
        value="help",
        screen_type="external",
        label="Help",
    ),
    DrawerScreen(
        value="live_chat",
        screen_type="external",
        label="Live Chat",
    ),
]


contact_us_drawer_app = DrawerApp(
    value="contact_us",
    label="Contact Us",
    screens={screen.value: screen for screen in _screens},
)
