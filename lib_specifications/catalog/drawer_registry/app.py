from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="app_registration_login",
        screen_type="external",
        label="App Registration Login",
    ),
    DrawerScreen(
        value="app_forced_update_required",
        screen_type="external",
        label="App Forced Update Required",
        is_active=False,
    ),
]

app_drawer_app = DrawerApp(
    value="app",
    label="App",
    screens={screen.value: screen for screen in _screens},
)
