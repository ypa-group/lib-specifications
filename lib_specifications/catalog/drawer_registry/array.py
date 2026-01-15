from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="ssn_info",
        screen_type="internal",
        label="SSN Info",
    ),
    DrawerScreen(
        value="preverification_info",
        screen_type="internal",
        label="Prequalification Info",
    ),
    DrawerScreen(
        value="security_info",
        screen_type="internal",
        label="Security Info",
    ),
    DrawerScreen(
        value="registration",
        screen_type="external",
        label="Registration",
    ),
    DrawerScreen(
        value="component_auth_start",
        screen_type="external",
        label="Component Auth Start",
    ),
    DrawerScreen(
        value="create_credit_history",
        screen_type="external",
        label="Create Credit History",
    ),
    DrawerScreen(
        value="failed_data",
        screen_type="external",
        label="Failed Data",
    ),
]

array_drawer_app = DrawerApp(
    value="array",
    label="Array",
    screens={screen.value: screen for screen in _screens},
)
