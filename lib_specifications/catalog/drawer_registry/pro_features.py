from ...core import DrawerApp, DrawerScreen

_screens = [
    DrawerScreen(
        value="freezing_question_mark",
        screen_type="internal",
        label="Freezing Question Mark",
        is_active=False,
    ),
    DrawerScreen(
        value="data_frozen_question_mark",
        screen_type="internal",
        label="Data Frozen Question Mark",
        is_active=False,
    ),
    DrawerScreen(
        value="pro_freezing_in_5_days",
        screen_type="external",
        label="Pro Freezing in 5 Days",
        is_active=False,
    ),
    DrawerScreen(
        value="cancel_pro_reasons",
        screen_type="external",
        label="Cancel Pro Reasons",
        is_active=False,
    ),
    DrawerScreen(
        value="short_description",
        screen_type="internal",
        label="Short Description",
    ),
    DrawerScreen(
        value="subscription_free_period_ends",
        screen_type="internal",
        label="Subscription Free Period Ends",
        is_active=False,
    ),
]

pro_features_drawer_app = DrawerApp(
    value="pro_features",
    label="Pro Features",
    screens={screen.value: screen for screen in _screens},
)
