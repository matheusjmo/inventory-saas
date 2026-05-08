from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class SKU:
    code: str

    def __post_init__(self) -> None:
        if not self.code or not self.code.replace("-", "").replace("_", "").isalnum():
            raise ValueError(f"Invalid SKU: {self.code}")
        object.__setattr__(self, "code", self.code.upper())


@dataclass(frozen=True)
class Price:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Price cannot be negative")
