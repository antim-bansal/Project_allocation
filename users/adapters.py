
       
# from allauth.account.adapter import DefaultAccountAdapter
# from .models import CustomUser
# from django.shortcuts import redirect
# from django.urls import reverse

# class CustomAccountAdapter(DefaultAccountAdapter):
#     def get_login_redirect_url(self, request):
#         user = request.user
#         if user.role == CustomUser.ROLE_STUDENT:
#            return reverse('student:add_student')
#         elif user.role == CustomUser.ROLE_PROFESSOR:
#               return reverse('professor:student_details')
#         return super().get_login_redirect_url(request)

#     def get_signup_redirect_url(self, request):
#         user = request.user
#         if user.role == CustomUser.ROLE_NONE:
#             return '/choose_role/{}/'.format(user.id)


from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser
from professor.models import Professor

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.role == CustomUser.ROLE_STUDENT:
            return reverse('student:professors_list')
        elif user.role == CustomUser.ROLE_PROFESSOR:
            # return reverse('professor:student_details')
            professor = Professor.objects.get(user=user)  # Access the related professor through the Professor model
            professor_id = professor.id
            redirect_url = reverse('professor:student_details', kwargs={'professor_id': professor_id})
            return redirect_url
        return super().get_login_redirect_url(request)

    def get_signup_redirect_url(self, request):
        user = request.user
        if user.role == CustomUser.ROLE_NONE:
            return reverse('choose_role', args=[user.id])
