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
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tasks = {}
            cls._instance._next_id = 1
        return cls._instance

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


class TaskFilter:
    label = ""
    empty_message = ""

    def apply(self, tasks):
        raise NotImplementedError


class AllTasks(TaskFilter):
    label = "All tasks"
    empty_message = "No tasks yet."

    def apply(self, tasks):
        return list(tasks)


class PendingTasks(TaskFilter):
    label = "Pending tasks"
    empty_message = "No pending tasks."

    def apply(self, tasks):
        return [task for task in tasks if not task.done]


class CompletedTasks(TaskFilter):
    label = "Completed tasks"
    empty_message = "No completed tasks."

    def apply(self, tasks):
        return [task for task in tasks if task.done]


class Command:
    label = ""
    exits_app = False

    def __init__(self):
        self.manager = TaskManager()

    def execute(self):
        raise NotImplementedError

    def print_tasks(self, task_filter):
        tasks = task_filter.apply(self.manager)

        if not tasks:
            print(task_filter.empty_message)
            return False

        for task in tasks:
            print(task)
        return True

    def ask_task_id(self, action):
        if not self.print_tasks(AllTasks()):
            return None

        try:
            task_id = int(input(f"Task id to {action}: "))
        except ValueError:
            print("Please enter a valid number.")
            return None

        if task_id < 1:
            print("Task id must be a positive number.")
            return None

        return task_id


class AddTaskCommand(Command):
    label = "Add Task"

    def execute(self):
        title = input("Task description: ").strip()

        if not title:
            print("Task description can't be empty.")
            return

        task = self.manager.add(title)
        print(f"Added: {task.title}")


class ListTasksCommand(Command):
    label = "List Tasks"

    def __init__(self):
        super().__init__()
        self.filters = {
            "1": AllTasks(),
            "2": PendingTasks(),
            "3": CompletedTasks(),
        }

    def execute(self):
        if len(self.manager) == 0:
            print("No tasks yet.")
            return

        for key, task_filter in self.filters.items():
            print(f"{key}. {task_filter.label}")

        choice = input("Choose a view: ").strip()
        task_filter = self.filters.get(choice)

        if task_filter is None:
            print(f"Invalid choice, please enter 1-{len(self.filters)}.")
            return

        self.print_tasks(task_filter)


class RemoveTaskCommand(Command):
    label = "Remove Task"

    def execute(self):
        task_id = self.ask_task_id("remove")
        if task_id is None:
            return

        task = self.manager.remove(task_id)
        if task is None:
            print(f"No task with id {task_id}.")
        else:
            print(f"Removed: {task.title}")


class ToggleTaskCommand(Command):
    label = "Mark Task Completed/Pending"

    def execute(self):
        task_id = self.ask_task_id("mark")
        if task_id is None:
            return

        task = self.manager.toggle(task_id)
        if task is None:
            print(f"No task with id {task_id}.")
        else:
            status = "completed" if task.done else "pending"
            print(f"Marked as {status}: {task.title}")


class ExitCommand(Command):
    label = "Exit"
    exits_app = True

    def execute(self):
        print("Goodbye!")


class TodoApp:
    def __init__(self):
        self.commands = {
            "1": AddTaskCommand(),
            "2": ListTasksCommand(),
            "3": RemoveTaskCommand(),
            "4": ToggleTaskCommand(),
            "5": ExitCommand(),
        }

    def show_menu(self):
        print("\n--- To-Do List ---")
        for key, command in self.commands.items():
            print(f"{key}. {command.label}")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()

            command = self.commands.get(choice)
            if command is None:
                print(f"Invalid choice, please enter 1-{len(self.commands)}.")
                continue

            command.execute()
            if command.exits_app:
                break


if __name__ == "__main__":
    TodoApp().run()