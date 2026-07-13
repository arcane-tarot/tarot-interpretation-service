from typing import Protocol


class TextGenerationError(Exception):
    pass


class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

    def is_ready(self) -> bool:
        raise NotImplementedError
