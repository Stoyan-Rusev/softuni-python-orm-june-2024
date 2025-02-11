import os
from datetime import date

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import RealEstateListing, VideoGame, BillingInfo, Invoice, Project, Programmer, Technology, Task

# Run and print your queries
# 4. Get recent completed tasks
recent_completed = task1.recent_completed_tasks(days=5)
print("Recent Completed Tasks:")
for task in recent_completed:
    print('- ' + task.title)
