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
from statistics import median, mode, mean, StatisticsError

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
                if line:
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

        elif tipo == "form-4":
            flag_form_4 = True
            file_data = archivo.read().decode("utf-8")
            lines = file_data.split("\n")
            list_edades = []
            list_pesos = []
            list_estatura = []
            for line in lines:
                if line:
                    fields = line.split(",")
                    list_edades.append(fields[0])
                    list_pesos.append(fields[2])
                    list_estatura.append(fields[3])
            list_edades.pop(0)
            list_pesos.pop(0)
            list_estatura.pop(0)

            list_edades_int = []
            for row in list_edades:
                list_edades_int.append(float(row))

            list_pesos_int = []
            for row in list_pesos:
                list_pesos_int.append(float(row))

            list_estatura_int = []
            for row in list_estatura:
                list_estatura_int.append(float(row))
            print(list_edades_int, list_pesos_int, list_estatura_int, "<-JA")
            #Moda
            try:
                edades_mode = mode(list_edades_int)
            except StatisticsError:
                edades_mode = "No unique mode found"
            try:
                pesos_mode = mode(list_pesos_int)
            except StatisticsError:
                pesos_mode = "No unique mode found"
            try:
                estaturas_mode = mode(list_estatura_int)
            except StatisticsError:
                estaturas_mode = "No unique mode found"

            # Media
            edades_media = mean(list_edades_int)
            pesos_media = mean(list_pesos_int)
            estaturas_media = mean(list_estatura_int)      
            # Mediana
            edades_mediana = median(list_edades_int)
            pesos_mediana = median(list_pesos_int)
            estaturas_mediana = median(list_estatura_int)

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

