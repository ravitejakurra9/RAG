# token_budget.py

class TokenBudget:
    def __init__(
        self,
        context_window: int,
        output_tokens: int,
        system_tokens: int = 150,
        user_tokens: int = 100,
        safety_margin: int = 200,
    ):
        self.context_window = context_window
        self.output_tokens = output_tokens
        self.system_tokens = system_tokens
        self.user_tokens = user_tokens
        self.safety_margin = safety_margin
        self._calculate()

    def _calculate(self):
        usable = (
            self.context_window
            - self.output_tokens
            - self.system_tokens
            - self.user_tokens
            - self.safety_margin
        )
        self.history_tokens = int(usable * 0.25)
        self.retrieval_tokens = int(usable * 0.75)

    def as_dict(self):
        return {
            "history_tokens": self.history_tokens,
            "retrieval_tokens": self.retrieval_tokens,
            "output_tokens": self.output_tokens,
        }
