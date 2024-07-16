from django.shortcuts import render
from .models import Article

def index(request):
	
	articles = Article.objects.filter(status='Published').order_by('-updated')
	context = {
		'articles': articles
	}
	return render(request, 'blog/index.html', context)


def detail(request, article_id, slug):
	
	article = Article.objects.get(id=article_id, slug=slug)
	context = {
		'article': article,
	}
	return render(request, 'blog/detail.html', context)


