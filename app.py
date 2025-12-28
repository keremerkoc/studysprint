from flask import Flask, render_template, request, redirect, url_for, flash
from core.task_manager import TaskManager

app = Flask(__name__)
app.secret_key = "dev-secret-key"


tm = TaskManager("data/tasks.json")


@app.get("/")
def home():
    tasks = tm.sort_for_display()
    return render_template("index.html", tasks=tasks)

@app.post("/tasks")
def create_task():
    title = request.form.get("title", "")
    priority_str = request.form.get("priority", "3")

    try:
        priority = int(priority_str)
        tm.add_task(title=title, priority=priority)
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("home"))



@app.post("/tasks/<int:task_id>/complete")
def complete_task(task_id: int):
    try:
        tm.complete(task_id)
    except KeyError:
        pass
    return redirect(url_for("home"))


@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id: int):
    try:
        tm.delete(task_id)
    except KeyError:
        pass
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
