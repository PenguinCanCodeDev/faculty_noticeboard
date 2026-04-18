from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from .models import Notice


def populate_notices():
    user = User.objects.first()

    if not user:
        user = User.objects.create_user(
            username="admin_seed",
            password="password123"
        )

    categories = ['EXAMS', 'LECTURES', 'EVENTS', 'SCORES', 'GENERAL']

    titles = [
        "Mid Semester Examination Schedule",
        "Faculty Weekly Lecture Update",
        "Departmental Orientation Event",
        "Supplementary Examination Results",
        "General Faculty Announcement",
        "Course Registration Reminder",
        "Guest Lecture Series",
        "Updated Academic Calendar",
        "Practical Lab Timetable",
        "Student Advisory Notice"
    ]

    bodies = [
        "Students should carefully read the notice and follow the instructions.",
        "Please check the schedule and prepare accordingly.",
        "This communication is issued by the faculty administration.",
        "Ensure compliance with academic regulations.",
        "Further updates will be provided soon."
    ]

    for i in range(10):
        Notice.objects.create(
            author=user,
            title=titles[i],
            body=random.choice(bodies),
            category=random.choice(categories),
            posted_date=timezone.now(),
            expiry_date=timezone.now().date() + timedelta(days=random.randint(7, 30)),
            is_important=random.choice([True, False]),
            view_password="" if random.choice([True, False]) else "faculty123"
        )

    print("10 notices created successfully.")