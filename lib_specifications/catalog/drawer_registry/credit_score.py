from ...core import DrawerApp, DrawerScreen, DrawerScreenOption

_screens = [
    DrawerScreen(
        value="info",
        screen_type="internal",
        label="Info",
    ),
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
        value="disable_btn",
        screen_type="external",
        label="Disable Button",
    ),
    DrawerScreen(
        value="demo",
        screen_type="external",
        label="Demo",
    ),
    DrawerScreen(
        value="factors",
        screen_type="external",
        label="Factors",
        options=[
            DrawerScreenOption(
                value="payment_history",
                label="Payment History",
            ),
            DrawerScreenOption(
                value="credit_card_utilization",
                label="Credit Card Utilization",
            ),
            DrawerScreenOption(
                value="credit_age",
                label="Credit Age",
            ),
            DrawerScreenOption(
                value="credit_accounts",
                label="Credit Accounts",
            ),
            DrawerScreenOption(
                value="credit_inquiries",
                label="Credit Inquiries",
            ),
            DrawerScreenOption(
                value="derogatory_marks",
                label="Derogatory Marks",
            ),
        ],
    ),
]


credit_score_drawer_app = DrawerApp(
    value="credit_score",
    label="Credit Score",
    screens={screen.value: screen for screen in _screens},
)
