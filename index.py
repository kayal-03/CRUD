from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Reading the book", "completed": False},
    {"id": 2, "title": "Update LinkedIn", "completed": False},
    {"id": 3, "title": "Complete the task", "completed": False},
    {"id": 4, "title": "Solve LeetCode", "completed": False},
]

next_id = 5


@app.route("/")
def index():
    incomplete = sum(1 for t in tasks if not t["completed"])
    completed_count = sum(1 for t in tasks if t["completed"])

    return render_template(
        "index_t.html",
        tasks=tasks,
        incomplete=incomplete,
        completed_count=completed_count
    )


@app.route("/add", methods=["POST"])
def add():
    global next_id
    title = request.form.get("title", "").strip()

    if title:
        tasks.append({
            "id": next_id,
            "title": title,
            "completed": False
        })
        next_id += 1

    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = not t["completed"]
            break

    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["POST"])
def edit(task_id):
    new_title = request.form.get("title", "").strip()

    if new_title:
        for t in tasks:
            if t["id"] == task_id:
                t["title"] = new_title
                break

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
