from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'body', 'category', 'expiry_date', 'attachment', 'is_important', 'view_password']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'body': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter notice details...'}),
        }