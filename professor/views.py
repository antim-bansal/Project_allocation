from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import ProfessorForm, ProjectForm
from .models import Project, Professor, Allocation, SelectedStudent, Deadline
from student.models import Student ,Notification
from django.core.mail import send_mail
import random
from django.utils import timezone

def projects(request, professor_id):
  
    professor = Professor.objects.get(id=professor_id)

    # Retrieve all projects associated with the professor
    projects = Project.objects.filter(professor=professor)

    return render(request, 'professor/projects.html', {'projects': projects, 'professor':professor})

def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            # Redirect to the projects view after saving the modifications
            return redirect('professor:projects', professor_id=project.professor.id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'professor/project_details.html', {'project': project, 'form': form})


# @login_required
# def professor_details(request):
#     if request.method == 'POST':
#         form = ProfessorForm(request.POST)
#         if form.is_valid():
#             current_user = request.user
#             professor = form.save(commit=False)
#             professor_id = professor.id
#             professor.user = current_user
#             professor.save()
#             message = "Changes saved!"
#             return redirect(reverse('professor:add_project', kwargs={'professor_id': professor_id}))  # Redirect to Add Project page
#     else:
#         form = ProfessorForm()

    # return render(request, 'professor/professor_details.html', {'form': form})
    
from django.shortcuts import redirect

def professor_details(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            current_user = request.user
            professor = form.save(commit=False)
            professor.user = current_user
            professor.save()
            message = "Changes saved!"
            # Consider redirecting to a success page or displaying a success message
            # return redirect(reverse('professor:success'))
            # return redirect('professor:add_project', kwargs={'professor_id': professor.id})
            return HttpResponseRedirect(reverse('professor:add_project', kwargs={'professor_id': professor.id}))
    else:
        form = ProfessorForm()

    return render(request, 'professor/professor_details.html', {'form': form})




# @login_required
# def professor_details(request):
#     if request.method == 'POST':
#         form = ProfessorForm(request.POST)
#         if form.is_valid():
#             professor = form.save(commit=False)
#             professor.user = request.user  # Assign the authenticated user directly
#             professor.save()
            
#             return redirect('professor:add_project', professor_id=professor.id)  # Redirect to Add Project page
#     else:
#         form = ProfessorForm()

#     return render(request, 'professor/professor_details.html', {'form': form})


# @login_required
def professor_profile(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    user = request.user
 
    previous_deadline = Deadline.default_deadline

    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()

            if professor.is_hod:  # Only process deadline modification if the professor is the HOD
                deadline_value = request.POST.get('deadline')
                if deadline_value:
                    # Save the deadline for project allocation
                    deadline, created = Deadline.objects.get_or_create()
                    deadline.deadline = deadline_value
                    deadline.save()

            return redirect('professor:student_details', professor_id=professor.id)
    else:
        form = ProfessorForm(instance=professor)
       
        previous_deadline_obj = Deadline.objects.first()
        if previous_deadline_obj:
            previous_deadline = previous_deadline_obj.deadline

    context = {
        'professor': professor,
        'form': form,
        'previous_deadline': previous_deadline,
        # 'student': student,
    }
    return render(request, 'professor/professor_profile.html', context)


from .models import Professor
from django.shortcuts import get_object_or_404

# @login_required
# def add_project(request, professor_id):
#     professor = Professor.objects.get(id=professor_id)
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             professor = get_object_or_404(Professor, user=request.user)
#             project = form.save(commit=False)
#             project.professor = professor
#             project.save()

#             if 'add_another' in request.POST:
#                 return redirect(reverse('professor:add_project', kwargs={'professor_id': professor_id}))  # Redirect to Add Project page to add another project
#             else:
#                 return redirect(reverse('professor:student_details', kwargs={'professor_id': professor_id}))  # Redirect to Student Details page if adding later # Redirect to Student Details page if adding later
#     else:
#         form = ProjectForm()
#         context = {
#         'professor': professor,
#         'form': form,
        
#     }
    

#     return render(request, 'professor/add_project.html', context)

# @login_required
def add_project(request, professor_id):
    professor = Professor.objects.get(id=professor_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            professor = get_object_or_404(Professor, user=request.user)
            project = form.save(commit=False)
            project.professor = professor
            project.save()

            if 'add_another' in request.POST:
                return redirect('professor:add_project', professor_id=professor.id)  # Redirect to Add Project page to add another project
            else:
                return redirect('professor:student_details', professor_id=professor.id) # Redirect to Student Details page if adding later
    else:
        form = ProjectForm()
        context = {
        'professor': professor,
        'form': form,
        
    }
    

    return render(request, 'professor/add_project.html', context)

# @login_required
def student_details(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    allocations = Allocation.objects.filter(professor=professor, selected=False)
    sort_by = request.GET.get('sort_by')

    if sort_by == 'cgpa':
        allocations = allocations.order_by('-student__cgpa')

    context = {
        'professor': professor,
        'allocations': allocations,
    }

    if not allocations.exists():
        context['no_allocations'] = True 

    # Adding document_url to each allocation's student
    for allocation in allocations:
        allocation.student.document_url = allocation.student.resume_link

    
    # deadline_time = Deadline.deadline
    # schedule_allocation_after_deadline.apply_async(args=[deadline_time])

    return render(request, 'professor/student_details.html', context)

def display_pdf_viewer(request, student_id):
    # Retrieve the student object from the database
    student = get_object_or_404(Student, pk=student_id)

    # Construct the file path using the document field of the student
    file_path = request.build_absolute_uri(student.document.url)

    return render(request, 'professor/pdf_viewer.html', {'file_path': file_path})


def selected_students(request, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    selected_students = SelectedStudent.objects.filter(professor=professor)

    return render(request, 'professor/selected_students.html', {'professor': professor, 'selected_students': selected_students})


def allocate_projects_after_deadline(request):

    deadline = Deadline.objects.first()
    if deadline is not None:  # Check if deadline is not None
    # Access the deadline attribute only if deadline is not None
        deadline_date = deadline.deadline

    else:
        deadline_date = Deadline.default_deadline

    current_time = timezone.now()
    current_user = request.user
    professor = Professor.objects.get(user=current_user)

    if current_time < deadline_date:
        message = "Allocation can only occur after the deadline has passed."
        context = {
            'professor': professor,
            'message': message,
            'deadline': deadline_date,  # Pass the deadline to the context
            'form':  ProfessorForm(instance=professor),  # Replace YourFormClass with the actual form class
            'previous_deadline': deadline_date,  # Assuming the professor has a previous_deadline attribute
        }
        return render(request, 'professor/professor_profile.html', context)
    else: 
        
        requests = Allocation.objects.all()

            # Divide requests into FCFS and CGPA lists
        fcfs_requests = []
        cgpa_requests = []

        for request in requests:
            # print("Request student name:", request.student.name)
            request.project.rem_students= request.project.max_students
            if request.project.professor.selection_method == 'FCFS':
                fcfs_requests.append(request)
            else:
                cgpa_requests.append(request)

        # Sort FCFS list based on request sent time
        fcfs_requests = sorted(fcfs_requests, key=lambda request: request.created_at)

        # Sort CGPA list based on highest CGPA
        cgpa_requests = sorted(cgpa_requests, key=lambda request: request.student.cgpa, reverse=True)
        
        # Allot students based on FCFS list
        for request in fcfs_requests:
            print("fcfs Request student name:", request.student.name)
            if request.project.rem_students > 0:
                existing_allocation = Allocation.objects.filter(student=request.student, selected=True).first()
                print("existing: existing_allocation.student.name")
                if existing_allocation:
                    print("comparing")
                    if request.priority > existing_allocation.priority:
                        continue  # Ignore the request as the student is already allotted with a higher priority
                    else:
                        existing_allocation.selected = False
                        existing_allocation.save()
                        SelectedStudent.objects.filter(student=existing_allocation.student, professor=existing_allocation.project.professor, project=existing_allocation.project).delete()
                        print("deleted,fcfs")
                request.selected = True
                # print("Request status:", request.selected)
                request.save()
                selected_student =SelectedStudent.objects.create(student=request.student, professor=request.project.professor, project=request.project)
                print("fcfs,selected:", selected_student.student.name)
                print("prof:" , selected_student.professor.name)
                request.project.rem_students -= 1
                request.project.save()

        # Allot students based on CGPA list
        for request in cgpa_requests:
            print("cgpa Request student name:", request.student.name)
            flag=0
            if not request.selected and request.project.rem_students > 0:
                existing_fcfs_request = Allocation.objects.filter(student=request.student, selected=True).first()

                if existing_fcfs_request:
                    print("comparing")
                    if request.priority > existing_fcfs_request.priority:
                        continue  # Ignore the request as the student is already allotted with a higher priority
                    else:
                        existing_fcfs_request.selected = False
                        existing_fcfs_request.save()
                        SelectedStudent.objects.filter(student=existing_fcfs_request.student, professor=existing_fcfs_request.project.professor, project=existing_fcfs_request.project).delete()
                        print("deleted,cgpa")
                request.selected = True
                # print("Request status:", request.selected)
                request.save()
                selected_student =SelectedStudent.objects.create(student=request.student, professor=request.project.professor, project=request.project)
                print("cgpa,selected:", selected_student.student.name)
                print("prof:" , selected_student.professor.name)
                request.project.rem_students -= 1
                request.project.save()  

        # Get all students
        all_students = Student.objects.all()

        # Get selected students
        selected_students = SelectedStudent.objects.values_list('student', flat=True)

        # Create a list of remaining students by removing selected students from the total student list
        remaining_students = all_students.exclude(id__in=selected_students)

        # Collect projects with remaining students
        projects_with_remaining_students = Project.objects.filter(rem_students__gt=0)

        # Create a list to store instances of projects
        project_instances = []

        # Create instances of projects based on the number of remaining students
        for project in projects_with_remaining_students:
            remaining_students_count = project.rem_students
            for _ in range(remaining_students_count):
                project_instances.append(project)

        # Shuffle the list of project instances
        random.shuffle(project_instances)

        # Iterate through the project instances and remaining students to create SelectedStudent instances
        for project, student in zip(project_instances, remaining_students):
            # Create a SelectedStudent instance for the current project and student
            SelectedStudent.objects.create(
                
                student=student,
                professor=project.professor,
                project=project,
                selection_date=timezone.now()
            )
            print("random")

        final_s = SelectedStudent.objects.all()
            

        for s in final_s:
            # Perform the allocation logic for each selected student from the SelectedStudent model
            # ...
            selected_student = SelectedStudent.objects.get(id=s.id)
            # Create a notification for the selected student
            Notification.objects.create(
                user=selected_student.student.user,  # Assuming the student has a user attribute
                message=f"You have been allotted project {selected_student.project.title} under professor {selected_student.project.professor.name}."  # Customize the message as needed
            )
    return redirect('professor:student_details', professor_id=professor.id)