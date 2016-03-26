from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db import models
from makestory.models import Image
from clarifai.client import ClarifaiApi
import json

# Create your views here.
def index(request):
    return render(request, 'makestory/index.html')
    
def process(request):
    if request.method == "GET":
        if 'inputURL' in request.GET:
            # Validation of image url
            imageURL = request.GET['inputURL']
            indexOfDot = rfind(".")
            extension = imageURL[indexOfDot:]
            
            
            extension3 = imageURL[-3:]
            extension4 = imageURL[-4:]
            if extension3 = 'jpgs'
            
            clarifai_api = ClarifaiApi() # assumes environment variables are set.
            result = clarifai_api.tag_images(imageURL)
            
            class_list = result['results'][0]['result']['tag']['classes']
            prob_list = result['results'][0]['result']['tag']['probs']
            
            
            
            return output(request, {image_output: 'image_output', text_output: 'text_output')
        else:
            return index(request)
    return fail(request)
    
def output(request):
    return render(request, 'makestory/output.html')
    
def fail(request):
    return render(request, 'makestory/fail.html')