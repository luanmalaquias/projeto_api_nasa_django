from datetime import date, datetime
import pytz
from django.db import models
import requests


class Apod(models.Model):
    date = models.DateField(primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)
    hdurl = models.URLField(max_length=500, null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    media_type = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return str(self.date)


    def criar(dados):
        try:
            Apod.objects.create(
                date = dados['date'],
                title = dados['title'],
                explanation = dados['explanation'],
                hdurl = dados['hdurl'],
                url = dados['url'],
                media_type = dados['media_type'],
            )
        except:
            try:
                Apod.objects.create(
                    date = dados['date'],
                    title = dados['title'],
                    explanation = dados['explanation'],
                    url = dados['url'],
                    media_type = dados['media_type'],
                )
            except:
                pass


    def getObjectOrRequest(data = None):
        dataHoje = date.today()        
        dataMinima = date(1995, 6, 16)

        # se não tiver pesquisa
        if not data:
            # procura no banco
            dados = Apod.objects.filter(date__icontains = str(dataHoje))

            # se nao encontrou e a hora é maior que duas da manhã, faz o request
            if not dados:
                if datetime.now().hour >= 2:
                    apodRequest = requests.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')
                    dadosJson = apodRequest.json()
                    Apod.criar(dadosJson)   
                    dados = Apod.objects.filter(date__icontains = str(dataHoje))
                else:
                    dados = Apod.objects.all().order_by('-date')
            return dados
        
        # se tiver pesquisa
        else:
            # procura no banco
            dados = Apod.objects.filter(date__icontains = str(data))
            dataRequest = date(int(data[0:4]), int(data[5:7]), int(data[8:10]))

            # precisa: dados, data da requisição maior e menor que os limites e a hora for maior que 2 da manhã
            if not dados:
                if dataRequest >= dataMinima and dataRequest <= date.today() and datetime.now().hour >= 2:
                    apodRequest = requests.get(f'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={str(data)}')
                    dadosJson = apodRequest.json()
                    Apod.criar(dadosJson)
                    dados = Apod.objects.filter(date__icontains = str(data))
                    if not dados:
                        dados = Apod.objects.all().order_by('-date')
                else:
                    dados = Apod.objects.all().order_by('-date')
        return dados


class MRP(models.Model):
    id = models.IntegerField(primary_key=True)
    sol = models.IntegerField(blank=True, null=True)
    earth_date = models.DateField(blank=True, null=True)
    camera_id = models.IntegerField(blank=True, null=True)
    camera_name = models.CharField(blank=True, null=True, max_length=50)
    camera_full_name = models.CharField(blank=True, null=True, max_length=100)
    url = models.URLField(max_length=500, null=False, blank=False)
    rover_id = models.IntegerField(blank=True, null=True)
    rover_name = models.CharField(blank=True, null=True, max_length=50)
    rover_landing_date = models.CharField(blank=True, null=True, max_length=50)
    rover_launch_date = models.CharField(blank=True, null=True, max_length=50)
    rover_status = models.CharField(blank=True, null=True, max_length=20)

    def __str__(self):
        return str(self.id)

    def criar(dados):
        MRP.objects.create(
            id = dados['id'],
            sol = dados['sol'],
            earth_date = dados['earth_date'],
            camera_id = dados['camera']['id'],
            camera_name = dados['camera']['name'],
            camera_full_name = dados['camera']['full_name'],
            url = dados['img_src'],
            rover_id = dados['rover']['id'],
            rover_name = dados['rover']['name'],
            rover_landing_date = dados['rover']['landing_date'],
            rover_launch_date = dados['rover']['launch_date'],
            rover_status = dados['rover']['status']
        )
    
    def getObjectOrRequest(sol, rover):
        dados = MRP.objects.filter(sol__icontains = sol, rover_name__icontains = rover).order_by('id')

        if not dados:
            mrpRequest = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&api_key=DEMO_KEY')
            requestJson = mrpRequest.json()
            for dados in requestJson['photos']:
                MRP.criar(dados)
            dados = MRP.objects.filter(sol__icontains = sol, rover_name__icontains = rover).order_by('id')
        
        return dados


class Ip(models.Model):
    ip = models.CharField(max_length=200, null=False, blank=False)
    dataHora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} // {str(self.dataHora)[0:10]} // {str(self.dataHora)[10:16]}"

#################################### nasa search
def getRequestNasaSearch(pesquisa):
    request = requests.get(f'https://images-api.nasa.gov/search?q={pesquisa}')
    json = request.json()['collection']['items']

    for item in json:        
        data = item['data'][0]['date_created']
        item['data'][0]['date_created'] = fixDate(data)

    json.sort(reverse=True, key=ordenar)

    return json

def ordenar(e):
    return e['data'][0]['date_created']

def getContextNasaSearch(dados, index):
    mediaLink = dados[index]['href']
    mediaRequest = requests.get(mediaLink)
    mediaJson = mediaRequest.json()
    video = None
    imagem = None
    audio = None

    for str in mediaJson:
        if str.find('mp4') >= 0:
            if video:
                pass
            video = str
        if str.find('jpg') >= 0:
            if imagem:
                pass
            imagem = str
        if str.find('mp3') >= 0:
            if audio:
                pass
            audio = str

    context = {'dados': dados[index], 'video': video, 'imagem': imagem, 'audio': audio}
    return context

def fixDate(data):
    data = f'{data[0:4]} {data[5:7]} {data[8:10]}'
    return data


#################################### crew members
def getCrew():
    request = requests.get('https://api.spacexdata.com/v4/crew')
    requestJson = request.json()
    context = {'membros':requestJson}
    return context