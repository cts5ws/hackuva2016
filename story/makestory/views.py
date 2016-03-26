from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'makestory/index.html')
    
def process(request):
    if request.method == "GET":
        if 'inputURL' in request.GET:
            imageURL = request.GET['inputURL']
            
        else:
            return index(request)
    return fail(request)
    
def output(request):
    return render(request, 'makestory/index.html')
    
def fail(request):
    return render(request, 'makestory/fail.html')