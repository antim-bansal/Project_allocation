from professor.models import Deadline
from .models import Student  # Import your Deadline model
from django.contrib.auth.models import AnonymousUser
def deadline_context(request):
    deadline = None
    deadline_obj = Deadline.objects.first()
    if deadline_obj:
        deadline = deadline_obj.deadline
    else:
        deadline=Deadline.default_deadline
    return {'deadline': deadline}


def student_id(request):
    student_id = None
    if request.user.is_authenticated and not isinstance(request.user, AnonymousUser):
        try:
            student = Student.objects.get(user=request.user)
            student_id = student.id
        except Student.DoesNotExist:
            pass
    return {'student_id': student_id}