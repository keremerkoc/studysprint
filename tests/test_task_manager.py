from datetime import date, timedelta

import pytest

from core.task_manager import TaskManager


def make_tm(tmp_path):
    return TaskManager(str(tmp_path / "tasks.json"))


def test_add_task_assigns_unique_ids(tmp_path):
    tm = make_tm(tmp_path)
    t1 = tm.add_task("Task 1")
    t2 = tm.add_task("Task 2")
    assert t1.id == 1
    assert t2.id == 2


def test_add_task_rejects_empty_title(tmp_path):
    tm = make_tm(tmp_path)
    with pytest.raises(ValueError):
        tm.add_task("   ")


def test_add_task_rejects_invalid_priority(tmp_path):
    tm = make_tm(tmp_path)
    with pytest.raises(ValueError):
        tm.add_task("Hello", priority=0)
    with pytest.raises(ValueError):
        tm.add_task("Hello", priority=6)


def test_complete_delete_and_missing_id(tmp_path):
    tm = make_tm(tmp_path)
    t = tm.add_task("Finish assignment")
    tm.complete(t.id)
    assert tm.get_by_id(t.id).completed is True

    tm.delete(t.id)
    with pytest.raises(KeyError):
        tm.get_by_id(t.id)


def test_due_today_and_upcoming(tmp_path):
    tm = make_tm(tmp_path)
    today = date.today()
    tomorrow = today + timedelta(days=1)

    tm.add_task("today task", due=today)
    tm.add_task("tomorrow task", due=tomorrow)

    assert len(tm.due_today()) == 1
    assert len(tm.upcoming()) == 1
