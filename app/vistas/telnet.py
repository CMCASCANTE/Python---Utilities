from django.http import HttpResponse
from django.shortcuts import render
import telnetlib 

def telnet(request):
    
    try:
        telnet = telnetlib.Telnet("212.227.85.30", 443)
        response = telnet
    except Exception as err:
        # print(err, file=sys.stderr)
        response = err
        
    return HttpResponse(render(request, "../templates/telnet.html", response))