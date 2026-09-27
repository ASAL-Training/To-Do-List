def show_menu():
    print("\n--- To-Do List ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Remove Task")
    print("4. Mark Task Completed/Pending")
    print("5. Exit")


def add_task(tasks):
    title = input("Task description: ").strip()

    if not title:
        print("Task description can't be empty.")
        return

    task = {"title": title, "done": False}
    tasks.append(task)
    print(f"Added: {title}")


def list_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return

    for number, task in enumerate(tasks, start=1):
        status = "x" if task["done"] else " "
        print(f"{number}. [{status}] {task['title']}")


def get_task_number(tasks, action):
    list_tasks(tasks)

    try:
        number = int(input(f"Task number to {action}: "))
    except ValueError:
        print("Please enter a valid number.")
        return None

    if number < 1 or number > len(tasks):
        print(f"No task with number {number}.")
        return None

    return number


def remove_task(tasks):
    if not tasks:
        print("No tasks to remove.")
        return

    number = get_task_number(tasks, "remove")
    if number is None:
        return

    removed = tasks.pop(number - 1)
    print(f"Removed: {removed['title']}")


def toggle_task(tasks):
    if not tasks:
        print("No tasks to update.")
        return

    number = get_task_number(tasks, "mark")
    if number is None:
        return

    task = tasks[number - 1]
    task["done"] = not task["done"]

    status = "completed" if task["done"] else "pending"
    print(f"Marked as {status}: {task['title']}")


def main():
    tasks = []

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(tasks)
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