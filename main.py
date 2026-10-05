class Task:
    def __init__(self, task_id, title):
        self.id = task_id
        self.title = title
        self.done = False

    def toggle(self):
        self.done = not self.done

    def __str__(self):
        status = "x" if self.done else " "
        return f"{self.id}. [{status}] {self.title}"


class TaskManager:
    def __init__(self):
        self._tasks = {}
        self._next_id = 1

    def __len__(self):
        return len(self._tasks)

    def __iter__(self):
        return iter(self._tasks.values())

    def add(self, title):
        task = Task(self._next_id, title)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def find(self, task_id):
        return self._tasks.get(task_id)

    def remove(self, task_id):
        return self._tasks.pop(task_id, None)

    def toggle(self, task_id):
        task = self.find(task_id)
        if task is not None:
            task.toggle()
        return task


class TodoApp:
    def __init__(self):
        self.manager = TaskManager()

    def show_menu(self):
        print("\n--- To-Do List ---")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Remove Task")
        print("4. Mark Task Completed/Pending")
        print("5. Exit")

    def add_task(self):
        title = input("Task description: ").strip()

        if not title:
            print("Task description can't be empty.")
            return

        task = self.manager.add(title)
        print(f"Added: {task.title}")

    def list_tasks(self):
        if len(self.manager) == 0:
            print("No tasks yet.")
            return

        for task in self.manager:
            print(task)

    def ask_task_id(self, action):
        self.list_tasks()

        try:
            task_id = int(input(f"Task id to {action}: "))
        except ValueError:
            print("Please enter a valid number.")
            return None

        if task_id < 1:
            print("Task id must be a positive number.")
            return None

        return task_id

    def remove_task(self):
        if len(self.manager) == 0:
            print("No tasks to remove.")
            return

        task_id = self.ask_task_id("remove")
        if task_id is None:
            return

        task = self.manager.remove(task_id)
        if task is None:
            print(f"No task with id {task_id}.")
        else:
            print(f"Removed: {task.title}")

    def toggle_task(self):
        if len(self.manager) == 0:
            print("No tasks to update.")
            return

        task_id = self.ask_task_id("mark")
        if task_id is None:
            return

        task = self.manager.toggle(task_id)
        if task is None:
            print(f"No task with id {task_id}.")
        else:
            status = "completed" if task.done else "pending"
            print(f"Marked as {status}: {task.title}")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.list_tasks()
            elif choice == "3":
                self.remove_task()
            elif choice == "4":
                self.toggle_task()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please enter 1-5.")


if __name__ == "__main__":
    TodoApp().run()