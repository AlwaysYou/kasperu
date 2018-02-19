from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import UserProfile
from xlrd import open_workbook
from .forms import RegisterForm
import os
import csv
# Create your views here.
from django.contrib.auth import login
from django.conf import settings
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
    userprofile = UserProfile.objects.get(user__id=request.user.id)

    flag_archivo = False
    if userprofile.archivo_csv:
        flag_archivo = True
        archivo = userprofile.archivo_csv
        # Falta: que solo muestre el archivo
    if request.method == "POST":
        tipo = request.POST.get('tipo_form')
        if tipo == "form-1":
            print(tipo, "<- tipo")
            userprofile = UserProfile.objects.get(user__id=request.user.id)
            userprofile.archivo_csv = request.FILES['Fichier1']
            userprofile.save()

        elif tipo == "form-2":
            file_data = archivo.read().decode("utf-8")
            lines = file_data.split("\n")
            lista_general = []
            for line in lines:
                fields = line.split(",")
                lista_general.append(fields)
        # conteo para completar las 50 filas
        numero_actual = len(lista_general)
        faltantes = 50 - numero_actual
        if faltantes > 0:
            rango = range(0, faltantes)

    return render(request, 'web/aplicativo.html', locals())

# muestra de CSV 50 filas

def mostrar_csv(request):
    userprofile = UserProfile.objects.get(user__id=request.user.id)
    archivo = userprofile.archivo_csv

    """ LEER EL ARCHIVO CSV"""
    ruta = os.path.join(settings.MEDIA_ROOT,
                        archivo.path)
    with open(ruta) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)

    return render(request, 'web/aplicativo.html', locals())
