from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from professor.models import Professor,Project, Allocation
from .models import Student, Notification 
from django.contrib import messages
from django.http import HttpResponse
from professor.models import Deadline


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            student = form.save(commit=False)
            student.user = current_user
            student.save()

            return redirect('student:professors_list')  # Redirect to the professors list page after successful submission
    else:
        form = StudentForm()
    return render(request, 'student/add_student.html', {'form': form})

def student_profile(request, student_id):
    student = Student.objects.get(id=student_id)
 
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student:professors_list')
    else:
        form = StudentForm(instance=student)
        
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'student/student_profile.html', context)


def professors_list(request):
    user = request.user
    student = Student.objects.get(user=user)
    professors = Professor.objects.all()
    current_user = request.user  # Assuming the current user is the student
    unseen_notifications_count = Notification.objects.filter(user=current_user, read=False).count()
    return render(request, 'student/professors_list.html', {'professors': professors, 'unseen_notifications_count': unseen_notifications_count ,'student':student,})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    professor = project.professor

    student = get_object_or_404(Student, user=request.user)
    request_sent = Allocation.objects.filter(project=project, student=student).exists()

    if request_sent:
        send_request_form = None  # No form if request has already been sent
        allocation = Allocation.objects.get(project=project, student=student)
    else:
        allocation = None
        send_request_form = SendRequestForm()  # Instantiate the form for sending the request

    return render(request, 'student/project_detail.html', {
        'professor': professor,
        'project': project,
        'send_request_form': send_request_form,
        'student': student,
        'request_sent': request_sent,
        'allocation': allocation  # Pass the form to the template
    })



from .forms import SendRequestForm  # Import the form for sending the request

def professor_detail(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    projects = Project.objects.filter(professor=professor)
    student = get_object_or_404(Student, user=request.user)  # Assuming 'user' is the ForeignKey to CustomUser in Student model
    
    return render(request, 'student/professor_detail.html', {
        'professor': professor,
        'projects': projects,
         # Pass the form to the template
    })










def send_request(request, project_id):
    allocation = None  # Initialize allocation as None
    success_message = ''  # Initialize success_message as an empty string

    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        student = get_object_or_404(Student, user=request.user)
        professor = project.professor  # Assuming professor is associated with the project
        
        # Acquire the priority from the request POST data
        priority = request.POST.get('priority', None)

        existing_allocation_with_priority = Allocation.objects.filter(student=student, priority=priority).first()

        if priority is not None and not existing_allocation_with_priority:  # Check if the priority is provided and no existing allocation with the same priority for the student
            # Create an instance in the Allocation model with priority and professor
            allocation, created = Allocation.objects.get_or_create(
                project=project,
                student=student,
                defaults={'selected': False, 'priority': priority, 'professor': professor}
            )
            success_message = 'Your request has been sent successfully!'
            messages.success(request, success_message)
        elif existing_allocation_with_priority:
            success_message = f'You have already sent a request with the same priority ({priority}) for another project.'
            messages.info(request, success_message)
        else:
            # Handle the case where priority is not acquired
            # You can add error messages or take other actions as needed
            pass

    return render(request, 'student/project_detail.html', {
        'allocation': allocation,
        'project': project,
        'success_message': success_message  # Pass the dynamic success message to the template
    })

# def send_request_success(request, professor_id):
#     # You can customize this view to display a success message or perform other actions after the request is sent
#     professor = Professor.objects.get(id=professor_id)
#     return render(request, 'professor/send_request_success.html', {'professor': professor})

def notifications(request):
    # Fetch notifications for the current student
    current_user = request.user  # Assuming the current user is the student
    notifications = Notification.objects.filter(user=current_user)
    notifications.update(read=True)
    student = Student.objects.get(user=current_user)
    # Render the notifications in a template
    return render(request, 'student/notifications.html', {
        'notifications': notifications,
        'student': student,  # Pass the student instance to the template context
    })


def sent_requests_list(request):
    user = request.user 
    student = Student.objects.get(user=user) 
    sent_requests = Allocation.objects.filter(student=student).order_by('priority')
    return render(request, 'student/sent_requests_list.html', {'sent_requests': sent_requests})

from django.shortcuts import render


from django.shortcuts import render
# from .models import Deadline

def my_view(request):
    # Fetch the earliest deadline from the Deadline model
    deadline = Deadline.objects.first()
    if deadline is not None:  # Check if deadline is not None
    # Access the deadline attribute only if deadline is not None
        deadline_date = deadline.deadline

    else:
        deadline_date = Deadline.default_deadline
    
    # Pass the deadline to the template context
    print(deadline_date)  # This will print the deadline in the console for debugging'
    print("dvcxvs")
    context = {
        'deadline': deadline_date
    }
    
    return render(request, 'student/student_base.html', context)

