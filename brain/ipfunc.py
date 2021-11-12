from nasafree.models import Ip
from datetime import datetime, timedelta



def getIp(request):    
    fowardedFor = request.META.get('HTTP_X_FORWARDED_FOR')    
    if fowardedFor:
        ip = fowardedFor.split(',')[0]        
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def verifyIp(request):
    # get ip in request
    userip = getIp(request)

    # get saved ip in database
    buscaBanco = Ip.objects.all().filter(ip=userip).order_by('-dataHora')

    if buscaBanco:
        # get time
        horaSalvaDoIp = buscaBanco[0].dataHora

        # get time now minus 1 hour of delay
        delay1h = datetime.now() - timedelta(hours=1)

        # compare and save
        if delay1h > horaSalvaDoIp:
            dado = Ip(ip=userip)
            dado.save()
    else:
        dado = Ip(ip=userip)
        dado.save()