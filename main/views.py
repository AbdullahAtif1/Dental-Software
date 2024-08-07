from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AppointmentForm, LoginForm
from django.http import JsonResponse
from dentadmin.models import Patient
from django.contrib.auth import authenticate, login

def index(request):
    form = AppointmentForm()
    loginform = LoginForm()

    if request.method == "POST":
        if request.user.is_authenticated:
            # Handle appointment form submission
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
            # Handle login form submission
            loginform = LoginForm(request.POST)
            if loginform.is_valid():
                username = loginform.cleaned_data['username']
                password = loginform.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                return redirect(request.path)

    context = {'form': form, 'lform': loginform}
    return render(request, 'main/index.html', context)
