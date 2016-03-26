from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from clarifai.client import ClarifaiApi
import json

# Create your views here.
def index(request):
    return render(request, 'makestory/index.html')
    
def process(request):
    # Validation of form
    if request.method == "GET":
        # Validation of request
        if 'inputURL' in request.GET:
            # Validation of image url
            imageURL = request.GET['inputURL']
            indexOfDot = rfind(".")
            indexOfDot += 1
            extension = imageURL[indexOfDot:]
            if extension != 'jpg' and extension != 'jpeg' and extension != 'png':
                return fail(request) # not a valid image (jpg, jpeg, png)
                
            clarifai_api = ClarifaiApi() # assumes environment variables are set.
            result = clarifai_api.tag_images(imageURL)
            
            class_list = result['results'][0]['result']['tag']['classes']
            prob_list = result['results'][0]['result']['tag']['probs']
            
            #currently just the list of matched words
            text_output = class_list.__str__()
            
            image_output = imageURL
            return render(request, 'makestory/output.html', {image_output:'image_output', text_output:'text_output'})
        else:
            return index(request)
    return fail(request)
    
def output(request):
    return render(request, 'makestory/output.html')
    
def fail(request):
    return render(request, 'makestory/fail.html')