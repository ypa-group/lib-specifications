from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="age_check",
        screen_type="internal",
        label="Age Check",
    ),
]

onboarding_drawer_app = DrawerApp(
    value="onboarding",
    label="Onboarding",
    screens={screen.value: screen for screen in _screens},
)
