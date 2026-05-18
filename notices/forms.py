from django import forms
from .models import Notice, NoticeAttachment

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'body', 'category', 'expiry_date', 'attachment', 'is_important', 'view_password']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'body': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter notice details...'}),
        }


class NoticeAttachmentForm(forms.ModelForm):
    class Meta:
        model = NoticeAttachment
        fields = ('file', 'file_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # file_name is hidden in the UI and auto-derived from the uploaded
        # filename in the view, so it must not be required at the form level.
        self.fields['file_name'].required = False