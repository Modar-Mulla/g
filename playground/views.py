from django.shortcuts import render

from django.shortcuts import render
from . import utils
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'index.html')
    
@csrf_exempt
def calc(request):
    if request.method == "POST":
        body = json.loads(request.body)
        popultaionSZ = int(body['popultaionSZ'])
        maxIter = int(body['maxIter'])
        candidatesol = int(body['candidatesol'])
        best = utils.start(popultaionSZ, maxIter, candidatesol)
        best = json.dumps(best)
        return HttpResponse(best)

