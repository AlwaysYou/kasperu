from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import UserProfile

from .forms import RegisterForm, LoginForm
import os
import csv
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from django.contrib.auth import login
from django.conf import settings
# histogram
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

#logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

def home(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.auth()
            if user:
                login(request, user)
                return redirect("web:aplicativo")
                print("LOGIN DENTOR DEL IF USER")
            else:
                print("NO EXISTE USER")
        else:
            print(form.errors, "<- errors")
            print("FORM INVALIDO")
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



@login_required(login_url=reverse_lazy('web:home'))
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
            userprofile = UserProfile.objects.get(user__id=request.user.id)
            if request.FILES.get('Fichier1'):
                userprofile.archivo_csv = request.FILES['Fichier1']
                userprofile.save()
                # Se guardo el archivo correctamente

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
            # falta si es positivo *
            if faltantes > 0:
                rango = range(0, faltantes)
                print(rango)

        elif tipo == "form-3":
            #Creacion de histogramas
            file_data = archivo.read().decode("utf-8")
            lines = file_data.split("\n")
            list_edades = []
            list_pesos = []
            list_estatura = []
            for line in lines:
                fields = line.split(",")
                list_edades.append(fields[0])
                list_pesos.append(fields[2])
                list_estatura.append(fields[3])
            list_edades[0] = '0'
            x = np.arange(len(list_edades))
            plt.bar(x, height=list_edades)
            plt.xticks(x, ["Edad 1", "Edad 2", "Edad 3", "Edad 4", "Edad 5"])
            f = plt.figure(1)
            plt.hist(x, normed=True, bins=15)

            plt.xlabel('X')
            plt.ylabel('Frequency')
            plt.title('Histograma de Edades')
            canvas = FigureCanvas(f)
            response = HttpResponse(content_type='image/png')
            canvas.print_png(response)
            plt.close()
            return response

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


@login_required(login_url=reverse_lazy('web:home'))
def user_logout(request):
    request.session.flush()
    return logout_then_login(request, reverse('web:home'))

