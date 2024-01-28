from celery.result import AsyncResult

# Replace 'your_task_id' with the actual task ID
result = AsyncResult('6e7d1e44-5827-47f6-a90c-dfef44b29bac')

if result.ready():
    print("Task has been completed.")
    print("Result:", result.result)
else:
    print("Task is still in progress.")
