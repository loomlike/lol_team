from dataclasses import dataclass


@dataclass
class PlayerRole:
    name: str
    role: str
    tier: int

    def __str__(self):
        return f"{self.role}: {self.name} ({self.tier})"
