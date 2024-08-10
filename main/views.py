from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import AppointmentForm, LoginForm
from django.http import JsonResponse
from dentadmin.models import Patient
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from dentadmin.forms import *
from django.contrib import messages

def index(request):
    form = AppointmentForm()
    loginform = LoginForm()

    if request.method == "POST":
        if request.user.is_authenticated:
            patient = Patient.objects.get(user=request.user)
            form = AppointmentForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.patient = patient
                instance.save()

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'message': "Your appointment is under review. We'll notify you soon in case of an update. Thank You"})
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'message': 'There was an error with your submission. Please try again later'}, status=400)
        else:
            loginform = LoginForm(request.POST)
            if loginform.is_valid():
                username = loginform.cleaned_data['username']
                password = loginform.cleaned_data['password']
                user = authenticate(
                    request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect(reverse('main:index'))
                else:
                    loginform.add_error(None, "Invalid username or password.")

    context = {'form': form, 'lform': loginform}
    return render(request, 'main/index.html', context)


def custom_logout(request):
    logout(request)
    # Redirect back to the same page
    return redirect(request.META.get('HTTP_REFERER', '/'))


def sigunp(request):

		s_form = CustomUserCreationForm()
		p_form = PatientForm()

		if request.method == "POST":
				s_form = CustomUserCreationForm(request.POST)
				p_form = PatientForm(request.POST)
				if s_form.is_valid() and p_form.is_valid():
						new_user = s_form.save()
						instance = p_form.save(commit=False)
						instance.email = new_user.email
						instance.user = new_user
						instance.save()
            
						#  Log the user in after signing up for a new account
						username = s_form.cleaned_data['username']
						password = s_form.cleaned_data['password1']
						user = authenticate(
                request, username=username, password=password
						)
						if user:
								login(request, user)
								messages.success(request, 'Your account has been successfully created!')
								return redirect(reverse('main:index'))
				else:
						print(s_form.errors)
						print(p_form.errors)
		else:
				s_form = CustomUserCreationForm()
				p_form = PatientForm()

		context = {'signupform': s_form, 'patientform': p_form}
		return render(request, 'main/signup.html', context)


class CustomPasswordResetView(auth_views.PasswordResetView):
    def get_success_url(self):
        return reverse_lazy('main:password_reset_done')

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
		def get_success_url(self):
			return reverse_lazy('main:password_reset_complete')
