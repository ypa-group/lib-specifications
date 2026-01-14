from typing import Protocol, runtime_checkable

from ...core import MiniApp, Trigger


@runtime_checkable
class OnboardingMiniAppProtocol(Protocol):
    YPIQS_INTRO: Trigger
    PRO_FEATURES_CREDIT_SCORE: Trigger
    PRO_FEATURES_BUDGET: Trigger
    PRO_FEATURES_CALCULATOR: Trigger
    NO_CARDS_AND_SCORE: Trigger
    ARRAY_PRECONNECT: Trigger
    ARRAY_CONNECT_DATA_ENTRY: Trigger
    ARRAY_PRE_VERIFICATION_SCREEN: Trigger
    ARRAY_VERIFICATION_CALLBACK_FAILED_DATA: Trigger
    ARRAY_VERIFICATION_CALLBACK_TOO_MANY_ATTEMPTS: Trigger
    ARRAY_VERIFICATION_CALLBACK_NO_CREDIT_HISTORY: Trigger
    ARRAY_VERIFICATION_CALLBACK_SUCCESS: Trigger
    ARRAY_CHECK_REPORT: Trigger
    ARRAY_QUIZ: Trigger
    ASSISTANTS_UNIVERSE: Trigger
    PLAID_PRECONNECT: Trigger
    PLAID_CONNECT: Trigger
    PLAID_CALLBACK_SUCCESS: Trigger
    PLAID_CHECK_REPORT: Trigger
    PLAID_WAITING_QUIZ_QUESTIONS: Trigger
    SKIP_PRO_FEATURES: Trigger


class OnboardingMiniApp(MiniApp, OnboardingMiniAppProtocol):
    pass


ONBOARDING: OnboardingMiniApp = MiniApp(
    name="ONBOARDING",
    description="Onboarding MiniApp",
)


# Register "ypiqs_intro" trigger
ONBOARDING.register_trigger(
    qualname="YPIQS_INTRO",
    description="YPIQS introduction screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)


# Register "SKIP_PRO_FEATURES" trigger
ONBOARDING.register_trigger(
    qualname="SKIP_PRO_FEATURES",
    description="Skip pro features trigger",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)


# Register "pro_features_credit_score" trigger
ONBOARDING.register_trigger(
    qualname="PRO_FEATURES_CREDIT_SCORE",
    description="Pro features credit score screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "pro_features_budget" trigger
ONBOARDING.register_trigger(
    qualname="PRO_FEATURES_BUDGET",
    description="Pro features budget screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "pro_features_calculator" trigger
ONBOARDING.register_trigger(
    qualname="PRO_FEATURES_CALCULATOR",
    description="Pro features calculator screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "no_cards_and_score" trigger
ONBOARDING.register_trigger(
    qualname="NO_CARDS_AND_SCORE",
    description="No cards and score screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_preconnect" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_PRECONNECT",
    description="Array preconnect screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_connect_data_entry" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_CONNECT_DATA_ENTRY",
    description="Array connect data entry screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_pre_verification_screen" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_PRE_VERIFICATION_SCREEN",
    description="Array pre-verification screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_verification_callback_failed_data" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_VERIFICATION_CALLBACK_FAILED_DATA",
    description="Array verification callback failed data",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_verification_callback_too_many_attempts" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_VERIFICATION_CALLBACK_TOO_MANY_ATTEMPTS",
    description="Array verification callback too many attempts",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_verification_callback_no_credit_history" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_VERIFICATION_CALLBACK_NO_CREDIT_HISTORY",
    description="Array verification callback no credit history",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_verification_callback_success" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_VERIFICATION_CALLBACK_SUCCESS",
    description="Array verification callback success",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_check_report" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_CHECK_REPORT",
    description="Array check report screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "array_quiz" trigger
ONBOARDING.register_trigger(
    qualname="ARRAY_QUIZ",
    description="Array quiz screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "assistants_universe" trigger
ONBOARDING.register_trigger(
    qualname="ASSISTANTS_UNIVERSE",
    description="Assistants universe screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "plaid_preconnect" trigger
ONBOARDING.register_trigger(
    qualname="PLAID_PRECONNECT",
    description="Plaid preconnect screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "plaid_connect" trigger
ONBOARDING.register_trigger(
    qualname="PLAID_CONNECT",
    description="Plaid connect screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "PLAID_CALLBACK_SUCCESS" trigger
ONBOARDING.register_trigger(
    qualname="PLAID_CALLBACK_SUCCESS",
    description="Plaid callback success screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "PLAID_CHECK_REPORT" trigger
ONBOARDING.register_trigger(
    qualname="PLAID_CHECK_REPORT",
    description="Plaid check report screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)

# Register "PLAID_WAITING_QUIZ_QUESTIONS" trigger
ONBOARDING.register_trigger(
    qualname="PLAID_WAITING_QUIZ_QUESTIONS",
    description="Plaid waiting quiz questions screen",
    context_schema=None,  # TODO: add context schema
    applicable_specifications=set(),  # TODO: add applicable specifications
)
