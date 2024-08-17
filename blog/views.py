from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import Article
from main import forms
from django.db.models import F, Value, Func
from django.db.models.functions import Lower
import random
from django.contrib.postgres.search import TrigramSimilarity

def index(request, name):

	ran_4 = list(Article.objects.filter(status='Published'))
	random.shuffle(ran_4)

	ran_4 = ran_4[:4]
	next_artcls = Article.objects.filter(status='Published')

	p = Paginator(next_artcls, 8)
	page_number = request.GET.get("page")

	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)

	word = request.GET.get('q')
	if word:

		word_lower = word.lower()
		next_artcls = Article.objects.annotate(
				similarity=TrigramSimilarity(Lower(F('title')), word_lower) + TrigramSimilarity(Lower(F('description')), word_lower)
		).filter(similarity__gt=0.3).order_by('-similarity', '-updated')

		print(next_artcls)

		p = Paginator(next_artcls, 8)
		page_number = request.GET.get("page")

		try:
			page_obj = p.get_page(page_number)
		except PageNotAnInteger:
			page_obj = p.page(1)
		except EmptyPage:
			page_obj = p.page(p.num_pages)

		context = {
			'next_artcls': next_artcls, 'word': word, 'page_obj': page_obj
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
			'ran_4': ran_4,
			'next_artcls': next_artcls,
			'form': form,
			'word': word,
			'page_obj': page_obj,
			'name': name
	}
	return render(request, 'blog/index.html', context)


def detail(request, article_id, slug, name):

	article = Article.objects.get(id=article_id, slug=slug)

	ran_4 = list(Article.objects.exclude(id=article_id))
	random.shuffle(ran_4)

	ran_4 = ran_4[:4]

	context = {
			'article': article,
			'others': ran_4,
			'name': name
	}
	return render(request, 'blog/detail.html', context)
