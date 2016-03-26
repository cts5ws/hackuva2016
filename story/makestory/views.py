from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'makestory/index.html')
    
def process(request):
    if request.method == "GET":
        return render(request, 'makestory/fail.html')
    return render(request, 'makestory/index.html')
    
def output(request):
    return render(request, 'makestory/index.html')
    
def fail(request):
    return render(request, 'makestory/fail.html')