from __future__ import annotations

import json
from pathlib import Path
from datetime import date
from typing import List, Optional

from core.task import Task


class TaskManager:
    def __init__(self, data_file: str = "data/tasks.json") -> None:
        self._tasks: List[Task] = []
        self._data_path = Path(data_file)
        self.load()

    def _reindex(self) -> None:
        """Ensure task IDs are always 1..n with no gaps."""
        # Keep current order by id (stable)
        self._tasks.sort(key=lambda t: t.id)
        for i, t in enumerate(self._tasks, start=1):
            t.id = i

    def add_task(self, title: str, due: Optional[date] = None, priority: int = 3) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        if not (1 <= priority <= 5):
            raise ValueError("Priority must be between 1 and 5.")

        new_id = len(self._tasks) + 1
        task = Task(id=new_id, title=title, due=due, priority=priority)
        self._tasks.append(task)

        self.save()
        return task

    def list_all(self) -> List[Task]:
        return list(self._tasks)

    def get_by_id(self, task_id: int) -> Task:
        for t in self._tasks:
            if t.id == task_id:
                return t
        raise KeyError(f"No task with id {task_id}")

    def complete(self, task_id: int) -> None:
        self.get_by_id(task_id).mark_done()
        self.save()

    def uncomplete(self, task_id: int) -> None:
        self.get_by_id(task_id).mark_undone()
        self.save()

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)
        self._tasks.remove(task)
        self._reindex()
        self.save()

    def due_today(self) -> List[Task]:
        today = date.today()
        return [t for t in self._tasks if t.due == today and not t.completed]

    def upcoming(self) -> List[Task]:
        today = date.today()
        return [t for t in self._tasks if t.due is not None and t.due > today and not t.completed]

    def completed(self) -> List[Task]:
        return [t for t in self._tasks if t.completed]

    def sort_for_display(self) -> List[Task]:
        """
        Sort order:
        1) incomplete first
        2) earlier due dates first (None goes last)
        3) higher priority first (1 is highest)
        """
        def sort_key(t: Task):
            due_sort = t.due if t.due is not None else date.max
            return (t.completed, due_sort, t.priority)

        return sorted(self._tasks, key=sort_key)

    def save(self) -> None:
        self._data_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "due": t.due.isoformat() if t.due else None,
                    "priority": t.priority,
                    "completed": t.completed,
                }
                for t in self._tasks
            ],
        }

        with self._data_path.open("w") as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        if not self._data_path.exists():
            return

        with self._data_path.open() as f:
            data = json.load(f)

        self._tasks = [
            Task(
                id=t["id"],
                title=t["title"],
                due=date.fromisoformat(t["due"]) if t.get("due") else None,
                priority=t["priority"],
                completed=t["completed"],
            )
            for t in data.get("tasks", [])
        ]
        self._reindex()
