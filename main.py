def show_menu():
    print("\n--- To-Do List ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Remove Task")
    print("4. Mark Task Completed/Pending")
    print("5. Exit")


def add_task(tasks, next_id):
    title = input("Task description: ").strip()

    if not title:
        print("Task description can't be empty.")
        return next_id

    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    print(f"Added: {title}")
    return next_id + 1


def list_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return

    for task in tasks:
        status = "x" if task["done"] else " "
        print(f"{task['id']}. [{status}] {task['title']}")


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def get_task_id(tasks, action):
    list_tasks(tasks)

    try:
        task_id = int(input(f"Task id to {action}: "))
    except ValueError:
        print("Please enter a valid number.")
        return None

    task = find_task(tasks, task_id)
    if task is None:
        print(f"No task with id {task_id}.")
        return None

    return task


def remove_task(tasks):
    if not tasks:
        print("No tasks to remove.")
        return

    task = get_task_id(tasks, "remove")
    if task is None:
        return

    tasks.remove(task)
    print(f"Removed: {task['title']}")


def toggle_task(tasks):
    if not tasks:
        print("No tasks to update.")
        return

    task = get_task_id(tasks, "mark")
    if task is None:
        return

    task["done"] = not task["done"]

    status = "completed" if task["done"] else "pending"
    print(f"Marked as {status}: {task['title']}")


def main():
    tasks = []
    next_id = 1

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            next_id = add_task(tasks, next_id)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            toggle_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-5.")


if __name__ == "__main__":
    main()