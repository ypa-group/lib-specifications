from typing import Protocol, runtime_checkable

from ...core import (
    ContextSchema,
    MiniApp,
    ParameterSchema,
    ParameterTypeEnum,
    Trigger,
)


@runtime_checkable
class BudgetMiniAppProtocol(Protocol):
    GENERIC: Trigger
    CUSTOMIZE: Trigger


class BudgetMiniApp(MiniApp, BudgetMiniAppProtocol):
    pass


BUDGET: BudgetMiniApp = MiniApp(
    name="BUDGET",
    description="Budget MiniApp",
)


# Register "CUSTOMIZE" trigger
BUDGET.register_trigger(
    qualname="CUSTOMIZE",
    description="Budget customize",
    context_schema=ContextSchema(
        parameters={
            "category_name": ParameterSchema(
                name="category_name",
                data_type=ParameterTypeEnum.STR,
                required=True,
            ),
            "amount": ParameterSchema(
                name="amount",
                data_type=ParameterTypeEnum.INT,
                required=True,
            ),
            "currency": ParameterSchema(
                name="currency",
                data_type=ParameterTypeEnum.STR,
                required=True,
            ),
            "period_type": ParameterSchema(
                name="period_type",
                data_type=ParameterTypeEnum.STR,
                required=False,
                default=None,
            ),
            "target_date": ParameterSchema(
                name="target_date",
                data_type=ParameterTypeEnum.DATE,
                required=False,
                default=None,
            ),
        }
    ),
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)


# Register "GENERIC" trigger
BUDGET.register_trigger(
    qualname="GENERIC",
    description="Budget generic",
    context_schema=None,  # TODO: add context schema
    applicable_callbacks=set(),  # TODO: add applicable callbacks
)
