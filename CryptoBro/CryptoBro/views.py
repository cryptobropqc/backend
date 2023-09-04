from django.shortcuts import render


def index(request):
    data = {
        'title': 'Cryptobro'
    }
    return render(request, 'index.html', data)


def blog(request):
    data = {
        'title': 'Cryptobro blog'
    }
    return render(request, 'blog.html', data)


def faq(request):
    data = {
        'title': 'Cryptobro FAQ'
    }
    return render(request, 'faq.html', data)
