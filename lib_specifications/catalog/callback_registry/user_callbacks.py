from ...core import BaseCallback


class HasOnboardedCallback(BaseCallback):
    """Check if a user has onboarded.
    Abstract callback that should be implemented in the evaluator environment.

    Args:
        auth_provider: The authentication provider
        auth_provider_user_id: The user ID from the authentication provider
    """

    qualname = "hasOnboarded"

    def __init__(self, auth_provider: str, auth_provider_user_id: str):
        self.auth_provider = auth_provider
        self.auth_provider_user_id = auth_provider_user_id

    def __call__(self) -> bool:
        raise NotImplementedError("This callback should be implemented in the evaluator environment.")


class HasPlaidInitializedCallback(BaseCallback):
    """Check if a user has a Plaid initialized.
    Abstract callback that should be implemented in the evaluator environment.

    Args:
        auth_provider: The authentication provider
        auth_provider_user_id: The user ID from the authentication provider
    """

    qualname = "hasPlaidInitialized"

    def __init__(self, auth_provider: str, auth_provider_user_id: str):
        self.auth_provider = auth_provider
        self.auth_provider_user_id = auth_provider_user_id

    def __call__(self) -> bool:
        raise NotImplementedError("This callback should be implemented in the evaluator environment.")


class HasConnectedCreditCardCallback(BaseCallback):
    """Check if a user has a credit card.
    Abstract callback that should be implemented in the evaluator environment.

    Args:
        auth_provider: The authentication provider
        auth_provider_user_id: The user ID from the authentication provider
    """

    qualname = "hasConnectedCreditCard"

    def __init__(self, auth_provider: str, auth_provider_user_id: str):
        self.auth_provider = auth_provider
        self.auth_provider_user_id = auth_provider_user_id

    def __call__(self) -> bool:
        raise NotImplementedError("This callback should be implemented in the evaluator environment.")


class HasArrayInitializedCallback(BaseCallback):
    """Check if a user has an Array initialized.
    Abstract callback that should be implemented in the evaluator environment.

    Args:
        auth_provider: The authentication provider
        auth_provider_user_id: The user ID from the authentication provider
    """

    qualname = "hasArrayInitialized"

    def __init__(self, auth_provider: str, auth_provider_user_id: str):
        self.auth_provider = auth_provider
        self.auth_provider_user_id = auth_provider_user_id

    def __call__(self) -> bool:
        raise NotImplementedError("This callback should be implemented in the evaluator environment.")


class HasCreditScoreCallback(BaseCallback):
    """Check if a user has a credit score.
    Abstract callback that should be implemented in the evaluator environment.

    Args:
        auth_provider: The authentication provider
        auth_provider_user_id: The user ID from the authentication provider
    """

    qualname = "hasCreditScore"

    def __init__(self, auth_provider: str, auth_provider_user_id: str):
        self.auth_provider = auth_provider
        self.auth_provider_user_id = auth_provider_user_id

    def __call__(self) -> bool:
        raise NotImplementedError("This callback should be implemented in the evaluator environment.")
