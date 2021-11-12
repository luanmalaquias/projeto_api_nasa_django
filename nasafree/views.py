from django.shortcuts import redirect, render
from .models import *
from datetime import date
from brain import ipfunc



def home(request):
    ipfunc.verifyIp(request)
    return render(request, 'views/nasa-spacex.html')


def apod(request):
    dados = Apod.getObjectOrRequest()
    buscaData = request.POST.get('data')
    if request.method == 'POST':
        dados = Apod.getObjectOrRequest(str(buscaData))    
    return render(request, 'views/apod.html', {'dados': dados[0]})


def marsWeather(request):
    return render(request, 'views/mars-weather.html')


def mrp(request):
    return render(request, 'views/mrp.html')

def mrpspirit(request):
    dados = MRP.objects.filter(sol = 1, rover_name__icontains = "spirit").order_by('id')
    buscaSol = request.POST.get('sol')
    if request.method == 'POST' and buscaSol:
        dados = MRP.getObjectOrRequest(buscaSol, "spirit")
    context = {'dados': dados, 'dias': 609}
    return render(request, 'views/mrpview.html', context)

def mrpopportunity(request):
    dados = MRP.objects.filter(sol = 1, rover_name__icontains = "opportunity").order_by('id')
    buscaSol = request.POST.get('sol')
    if request.method == 'POST' and buscaSol:
        dados = MRP.getObjectOrRequest(buscaSol, "opportunity")
    context = {'dados': dados, 'dias': 5100}
    return render(request, 'views/mrpview.html', context)

def mrpcuriosity(request):
    dias = date.today() - date(2012, 8, 6) 
    dados = MRP.objects.filter(sol = 1, rover_name__icontains = "curiosity").order_by('id')
    buscaSol = request.POST.get('sol')
    if request.method == 'POST' and buscaSol:
        dados = MRP.getObjectOrRequest(buscaSol, "curiosity")
    context = {'dias': dias.days - 90, 'dados': dados}
    return render(request, 'views/mrpview.html', context)

def trekImagery(request):
    return render(request, 'views/trek-imagery.html')

def nasaSearch(request):
    dados = None
    pesquisa = request.GET.get('q')

    if pesquisa:
        dados = getRequestNasaSearch(pesquisa)

    if request.method == 'POST':
        index = int(request.POST.get('index'))
        contextContent = getContextNasaSearch(dados, index)
        return render(request, 'views/search-content.html', contextContent)

    context = {'pesquisa': pesquisa, 'dados': dados}
    return render(request, 'views/search.html', context)

def crewMembers(request):
    context = getCrew()
    return render(request, 'views/crewmembers.html', context)

def handlerErrorPage(request, exception):
    return render(request, 'views/404.html')