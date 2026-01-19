from uuid import UUID

from ..core import (
    BudgetAlertWidget,
    BudgetCategoryAmountWidget,
    CreditCardSummaryWidget,
    CreditScoreValueWidget,
    DebtFreeTimeWidget,
    LanguageSelectorWidget,
    ParameterTypeEnum,
    PaymentReminderWidget,
    WidgetRegistry,
)

# Template widgets for the registry - these are used as examples/templates
# Each widget gets a placeholder UUID for registry purposes
WIDGETS_REGISTRY: WidgetRegistry = WidgetRegistry(
    [
        LanguageSelectorWidget(
            id=UUID("00000000-0000-0000-0000-000000000001"),
        ),
        CreditScoreValueWidget(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            params={
                "current_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 0,
                },
                "previous_score_value": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 0,
                },
            },
        ),
        BudgetCategoryAmountWidget(
            id=UUID("00000000-0000-0000-0000-000000000003"),
            params={
                "category_name": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "amount": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 0,
                },
                "currency": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
            },
        ),
        CreditCardSummaryWidget(
            id=UUID("00000000-0000-0000-0000-000000000004"),
            params={
                "bank_name": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "bank_logo": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "card_id": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "card_last_digits": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "amount": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 0,
                },
            },
        ),
        PaymentReminderWidget(
            id=UUID("00000000-0000-0000-0000-000000000005"),
            params={
                "bank_name": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "bank_logo": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "card_id": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "card_last_digits": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "payment_amount": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 0,
                },
                "due_date": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.DATE.label,
                    "value": "2025-01-01",
                },
            },
        ),
        BudgetAlertWidget(
            id=UUID("00000000-0000-0000-0000-000000000006"),
            params={
                "category_name": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "category_icon": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "spent_amount": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 0,
                },
            },
        ),
        DebtFreeTimeWidget(
            id=UUID("00000000-0000-0000-0000-000000000007"),
            params={
                "years": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 0,
                },
                "months": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.INT.label,
                    "value": 0,
                },
                "card_id": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
                "payment_strategy": {
                    "parameter_type": "value",
                    "data_type": ParameterTypeEnum.STR.label,
                    "value": "",
                },
            },
        ),
    ]
)
