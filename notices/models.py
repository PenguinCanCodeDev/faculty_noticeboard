from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notice(models.Model):
    # Category options as defined in the project requirement
    CATEGORY_CHOICES = [
        ('EXAMS', 'Exams'),
        ('LECTURES', 'Lectures/Schedules'),
        ('EVENTS', 'Events'),
        ('SCORES', 'Exam Scores / Supplementary Results'),
        ('GENERAL', 'General'),
    ]

    # Links notice to a specific Faculty Staff member
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices')
    
    # Core Content
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='GENERAL')
    
    # Timing & Management
    posted_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)
    
    # File Handling (PDFs, Excel, etc.)
    attachment = models.FileField(upload_to='notices/attachments/', null=True, blank=True)
    
    # UX & Security Logic
    is_important = models.BooleanField(default=False)
    view_password = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Required for securing Exam Score sheets specifically."
    )

    def __str__(self):
        return self.title

    class Meta:
        # Ensures newest notices appear at the top of the board
        ordering = ['-posted_date']

class NoticeAttachment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='notices/attachments/')
    file_name = models.CharField(max_length=100, help_text="Example: Chapter 1, Full Report, etc.")

    def __str__(self):
        return f"{self.file_name} for {self.notice.title}"