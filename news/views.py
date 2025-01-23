from django.shortcuts import render

from .models import News


def news_list(request):
    context = {'title': 'ElectroHub - News', 'news': News.objects.all().order_by('-created_at')}
    return render(request, "news/news_list.html", context)
