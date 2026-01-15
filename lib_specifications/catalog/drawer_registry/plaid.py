from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="security_info",
        screen_type="internal",
        label="Security Info",
    ),
    DrawerScreen(
        value="why_connect_plaid",
        screen_type="internal",
        label="Why Connect Plaid",
    ),
    DrawerScreen(
        value="connection_guide",
        screen_type="internal",
        label="Connection Guide",
    ),
    DrawerScreen(
        value="question_mark",
        screen_type="internal",
        label="Question Mark",
        is_active=False,
    ),
    DrawerScreen(
        value="linking_cards",
        screen_type="external",
        label="Linking Cards",
    ),
    DrawerScreen(
        value="phone_verification",
        screen_type="external",
        label="Phone Verification",
        is_active=False,
    ),
]
plaid_drawer_app = DrawerApp(
    value="plaid",
    label="Plaid",
    screens={screen.value: screen for screen in _screens},
)
