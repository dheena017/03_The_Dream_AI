import random

tasks = []

# Add deterministic tasks for verification
tasks.append("Calculate 50 + 50")
tasks.append("Calculate 10 * 10")
tasks.append("Write a script to reverse the string 'verification'")

# Category 1: Math
for i in range(250):
    a = random.randint(1, 1000)
    b = random.randint(1, 1000)
    op = random.choice(['+', '-', '*', '/'])
    tasks.append(f"Calculate {a} {op} {b}")

# Category 2: String Manipulation
words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]
for i in range(250):
    target = random.choice(words)
    action = random.choice(["reverse", "uppercase", "count vowels in", "find length of"])
    tasks.append(f"Write a script to {action} the string '{target}'")

# Category 3: List Operations
for i in range(250):
    length = random.randint(5, 20)
    lst = [random.randint(1, 100) for _ in range(length)]
    action = random.choice(["sort", "find max in", "find min in", "sum"])
    tasks.append(f"{action} this list: {lst}")

# Category 4: File Operations
for i in range(250):
    filename = f"test_file_{i}.txt"
    content = f"Content for file {i}"
    tasks.append(f"Create a file named '{filename}' with content '{content}'")

# Ensure we have roughly 1000 (plus the 3 extra)
with open("brain/tasks.txt", "w") as f:
    for task in tasks:
        f.write(task + "\n")

print(f"Generated {len(tasks)} tasks in brain/tasks.txt")
