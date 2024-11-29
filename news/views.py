from django.shortcuts import render

from django.shortcuts import render
from .models import News

def news_list(request):
    context = {'news':News.objects.all()}
    return render(request, "news/news_list.html", context)