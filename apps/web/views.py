from django.shortcuts import render

# Create your views here.

def home(request):

    return render(request, 'web/home.html', locals())

def create_account(request):
    return render(request, 'web/create_account.html', locals())


def aplicativo(request):
    return render(request, 'web/aplicativo.html', locals())

