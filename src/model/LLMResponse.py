class LLMResponse:
    def __init__(self, model: str, created_at: str, response: str, done: bool):
        self.model = model
        self.created_at = created_at
        self.response = response
        self.done = done