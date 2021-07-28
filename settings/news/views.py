from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.shortcuts import render, redirect
from .models import Article
from .parser import parse_urls

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import timedelta
from datetime import datetime
import django_rq

queue = Queue(name='default', connection=Redis())
job = queue.enqueue_in(timedelta(minutes=5), parse_urls)


def show_all_news(request):

    news = Article.objects.all()
    paginator = Paginator(news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news-list.html', {"page": page_obj})

def sync_news(request):

    parse_urls()
    return redirect('/')

def ArticleEuroDetail(request, pk):
    euro = Article.objects.get(pk=pk)
    return render(request, 'news/detail-article.html', {'rec': euro})

