from ..core import (
    BudgetAlertWidget,
    BudgetCategoryAmountWidget,
    CreditCardSummaryWidget,
    CreditScoreValueWidget,
    DebtFreeTimeWidget,
    LanguageSelectorWidget,
    PaymentReminderWidget,
    WidgetRegistry,
)

# Widget types registry - maps widget type strings to widget classes
WIDGET_REGISTRY: WidgetRegistry = WidgetRegistry(
    {
        "language_selector": LanguageSelectorWidget,
        "credit_score_value": CreditScoreValueWidget,
        "budget_category_amount": BudgetCategoryAmountWidget,
        "credit_card_summary": CreditCardSummaryWidget,
        "payment_reminder": PaymentReminderWidget,
        "budget_alert": BudgetAlertWidget,
        "debt_free_time": DebtFreeTimeWidget,
    }
)
