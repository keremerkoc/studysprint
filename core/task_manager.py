from __future__ import annotations

from datetime import date
from typing import List, Optional

from core.task import Task


class TaskManager:
    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, due: Optional[date] = None, priority: int = 3) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        if not (1 <= priority <= 5):
            raise ValueError("Priority must be between 1 and 5.")

        task = Task(id=self._next_id, title=title, due=due, priority=priority)
        self._tasks.append(task)
        self._next_id += 1
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

    def uncomplete(self, task_id: int) -> None:
        self.get_by_id(task_id).mark_undone()

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)
        self._tasks.remove(task)

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
