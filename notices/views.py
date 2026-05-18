from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Notice, NoticeAttachment
from .forms import NoticeForm, NoticeAttachmentForm
from django.utils import timezone
from django.db.models import Q
import os

AttachmentFormSet = inlineformset_factory(
    Notice, NoticeAttachment,
    form=NoticeAttachmentForm,
    extra=1, can_delete=True
)

@login_required
def staff_dashboard(request):
    # Only show notices created by the logged-in staff member
    notices = Notice.objects.filter(author=request.user).order_by('-posted_date')
    return render(request, 'staff/dashboard.html', {'notices': notices})

@login_required
def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        formset = AttachmentFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            
            # Save attachments with auto-naming logic
            instances = formset.save(commit=False)
            for instance in instances:
                instance.notice = notice
                # If the user didn't provide a name (since it's hidden), use the filename
                if not instance.file_name:
                    instance.file_name = instance.file.name
                instance.save()
            
            # Handle deletions
            for obj in formset.deleted_objects:
                obj.delete()
                
            return redirect('staff_dashboard')
    else:
        form = NoticeForm()
        formset = AttachmentFormSet()
    
    return render(request, 'staff/notice_form.html', {'form': form, 'formset': formset, 'title': 'Post New Notice'})

@login_required
def delete_notice(request, pk):
    # Ensure the staff member can only delete their own notice
    notice = get_object_or_404(Notice, pk=pk, author=request.user)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice deleted.")
        return redirect('staff_dashboard')
    return render(request, 'staff/confirm_delete.html', {'notice': notice})


def home(request):
    today = timezone.now().date()
    
    notices = Notice.objects.filter(
        Q(expiry_date__gte=today) | Q(expiry_date__isnull=True)
    ).order_by('-posted_date')

    query = request.GET.get('q')
    if query:
        notices = notices.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

    cat_filter = request.GET.get('category')
    if cat_filter:
        notices = notices.filter(category=cat_filter)
    
    paginator = Paginator(notices, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'public/home.html', {
        'notices': page_obj,
        'categories': Notice.CATEGORY_CHOICES
    })
    

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    access_granted = True
    error_msg = None

    # Logic for the Password Gate
    if notice.view_password:
        access_granted = False  # Lock it by default
        
        if request.method == "POST":
            entered_pwd = request.POST.get('password')
            if entered_pwd == notice.view_password:
                access_granted = True
            else:
                error_msg = "Incorrect password. Please contact the department."

    return render(request, 'public/detail.html', {
        'notice': notice,
        'access_granted': access_granted,
        'error_msg': error_msg
    })

@login_required
def edit_notice(request, pk):
    # Ensure only the author can edit
    notice = get_object_or_404(Notice, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice updated successfully!")
            return redirect('staff_dashboard')
    else:
        form = NoticeForm(instance=notice)
    
    return render(request, 'staff/notice_form.html', {
        'form': form, 
        'title': 'Edit Notice'
    })


def file_viewer(request, notice_id, file_type, file_id=None):
    notice = get_object_or_404(Notice, id=notice_id)
    
    try:
        if file_type == 'main':
            # CHECK: Does the main attachment actually exist?
            if not notice.attachment:
                messages.error(request, "This notice does not have a main attachment to view.")
                return redirect('notice_detail', pk=notice.id)
            
            file_url = notice.attachment.url
            file_name = "Main Attachment"
        else:
            attachment = get_object_or_404(NoticeAttachment, id=file_id)
            # CHECK: Does the sub-attachment file actually exist?
            if not attachment.file:
                messages.error(request, "The requested file is missing.")
                return redirect('notice_detail', pk=notice.id)
                
            file_url = attachment.file.url
            file_name = attachment.file_name

        # Logic for Image vs PDF remains the same
        ext = os.path.splitext(file_url)[1].lower()
        is_image = ext in ['.jpg', '.jpeg', '.png', '.gif']

        return render(request, 'public/viewer.html', {
            'file_url': file_url,
            'file_name': file_name,
            'is_image': is_image,
            'notice': notice,
            'file_type': file_type,
            'file_id': int(file_id) if file_id else None
        })

    except ValueError:
        messages.error(request, "There was an error accessing the file.")
        return redirect('notice_detail', pk=notice.id)