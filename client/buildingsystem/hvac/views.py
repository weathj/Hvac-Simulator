from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
from hvac.utils.client import Client
from .forms import *


ip_address = "127.0.0.1"
port = 7880

# Create your views here.

def index(request):
    request_strings = ["getAHUSATemp" , "getAHURATemp", "getOATemp", "getMADPRPos", "getOADPRPos", "getSAFANSpeed", "getRAFANSpeed", "getCLGCOILTemp", "getHTGCOILTemp"]
    response_strings = ["AHUSATemp" , "AHURATemp", "OATemp", "MADPRPos", "OADPRPos", "SAFANSpd", "RAFANSpd", "CLGCOILTemp", "HTGCOILTemp"]
    var_names = ["sa_temp" , "ra_temp", "oa_temp", "madpr_pos", "oadpr_pos", "safan_spd", "rafan_spd", "clgcoil_temp", "htgcoil_temp"]
    context ={}
    pos = 0
    for x in request_strings:
        request_data = {x: True}
        request_json = json.dumps(request_data)  # Serialize the request to JSON
        client = Client(ip_address, port)
        client.send(request_json + "\n")
        response = client.receive()
        response_data = json.loads(response)  # Parse the response JSON
        temp = {
            var_names[pos] : response_data[response_strings[pos]]
        }
        context.update(temp)
        pos = pos + 1
    client.close()
    print(context)

    if request.method == 'POST':
        print(request.POST)
        form = SAForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['sa_temp'])
            request_data = {"setAHUSATemp": form.cleaned_data['sa_temp']}
            request_json = json.dumps(request_data)  # Serialize the request to JSON
            client = Client(ip_address, port)
            client.send(request_json + "\n")
            response = client.receive()
            response_data = json.loads(response)
            temp = {
                "sa_temp" : response_data["AHUSATemp"]
            }
            context.update(temp)
            print(response_data)
            client.close()
            return render(request, 'index.html', context = context)

    return render(request, 'index.html', context = context)

# print(index(client = Client(ip_address, port).send(json.dumps(data = {
#         "getTemperature": True,
#     }) + "\n").receive().close()))