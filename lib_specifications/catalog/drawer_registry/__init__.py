from ...core import DrawerRegistry
from .app import app_drawer_app
from .array import array_drawer_app
from .assistant_corporation import assistant_corporation_drawer_app
from .budget import budget_drawer_app
from .calculator import calculator_drawer_app
from .contact_us import contact_us_drawer_app
from .credit_score import credit_score_drawer_app
from .faq import faq_drawer_app
from .modals import modals_drawer_app
from .onboarding import onboarding_drawer_app
from .plaid import plaid_drawer_app
from .pro_features import pro_features_drawer_app
from .ypiqs import ypiqs_drawer_app

drawer_apps = [
    app_drawer_app,
    array_drawer_app,
    assistant_corporation_drawer_app,
    budget_drawer_app,
    calculator_drawer_app,
    credit_score_drawer_app,
    contact_us_drawer_app,
    faq_drawer_app,
    modals_drawer_app,
    onboarding_drawer_app,
    plaid_drawer_app,
    pro_features_drawer_app,
    ypiqs_drawer_app,
]

DRAWER_REGISTRY = DrawerRegistry(drawer_apps)
