from django.shortcuts import render
from .forms import AppointmentForm
from django.http import JsonResponse
from dentadmin.models import Patient

def index(request):

	
	form = AppointmentForm()
	if request.method == "POST":
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
		form = AppointmentForm()

	context = {'form': form}

	return render(request, 'main/index.html', context)

