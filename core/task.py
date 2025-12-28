from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    due: Optional[date] = None
    priority: int = 3  # 1=high, 5=low
    completed: bool = False

    def mark_done(self) -> None:
        self.completed = True

    def mark_undone(self) -> None:
        self.completed = False
