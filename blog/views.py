from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import Article
from main import forms
from django.db.models import Q
import random


def index(request):

	frst_3 = list(Article.objects.all())
	random.shuffle(frst_3)

	frst_3 = frst_3[:3]
	next_artcls = Article.objects.all().order_by("-updated")

	p = Paginator(next_artcls, 6)
	page_number = request.GET.get("page")

	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)

	search = request.GET.get('q')
	if search:
		print(search)
		next_artcls = Article.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))

		p = Paginator(next_artcls, 6)
		page_number = request.GET.get("page")

		try:
			page_obj = p.get_page(page_number)
		except PageNotAnInteger:
			page_obj = p.page(1)
		except EmptyPage:
			page_obj = p.page(p.num_pages)

		context = {
			'next_artcls': next_artcls, 'search': search, 'page_obj': page_obj
		}
		return render(request, 'blog/index.html', context)

	form = forms.SubscriberForm()
	if request.method == 'POST':
			form = forms.SubscriberForm(request.POST)
			if form.is_valid():
					form.save()
					if request.headers.get('x-requested-with') == 'XMLHttpRequest':
							return JsonResponse({'message': 'Thank you for subscribing!'})
			else:
					if request.headers.get('x-requested-with') == 'XMLHttpRequest':
							return JsonResponse({'message': 'There was an error with your submission. Please try again later'}, status=400)
	else:
			form = forms.SubscriberForm()

	context = {
			'frst_3': frst_3,
			'next_artcls': next_artcls,
			'form': form,
			'search': search,
			'page_obj': page_obj
	}
	return render(request, 'blog/index.html', context)


def detail(request, article_id, slug):

	article = Article.objects.get(id=article_id, slug=slug)
	context = {
			'article': article,
	}
	return render(request, 'blog/detail.html', context)
