from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    name: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Category name cannot be empty")
        object.__setattr__(self, "name", self.name.strip().lower())
