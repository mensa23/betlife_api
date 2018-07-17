class ProfitResponse:
    def __init__(self, probabilities, profits, **kwargs):
        self.probabilities = probabilities
        self.profits = profits

        for k, v in kwargs.items():
            setattr(self, k, v)
