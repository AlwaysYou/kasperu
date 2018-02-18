from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import UserProfile
from .forms import RegisterForm
# Create your views here.
from django.contrib.auth import login

def home(request):

    return render(request, 'web/home.html', locals())

def create_account(request):

    profile_form = RegisterForm(request.POST)
    if request.method == "POST":
        print("soy post")
        if profile_form.is_valid():
            print("soy valido")
            # Falta validar las contrasenas en el js
            password = request.POST['password']
            profile_form.save(password)

            user = profile_form.auth(password)
            login(request, user)
            return redirect(reverse('web:aplicativo'))
        else:
            print("FALSO no es valido este profile")
            profile_form = RegisterForm()
            return HttpResponseRedirect("/?error/")
    return render(request, 'web/create_account.html', locals())


def aplicativo(request):
    flag_archivo = False

    userprofile = UserProfile.objects.get(user__id=request.user.id)
    if userprofile.archivo_csv:
        flag_archivo = True
        archivo = userprofile.archivo_csv
        # Falta: que solo muestre el archivo
        print(archivo, "<- file name")
    if request.method == "POST":
        print(request.FILES, "<- files")
        userprofile = UserProfile.objects.get(user__id=request.user.id)
        userprofile.archivo_csv = request.FILES['Fichier1']
        userprofile.save()

    return render(request, 'web/aplicativo.html', locals())

