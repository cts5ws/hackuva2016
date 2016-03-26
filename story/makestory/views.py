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
            indexOfDot = imageURL.rfind(".")
            if indexOfDot == -1:
                return fail(request) # not an image URL
            indexOfDot += 1
            extension = imageURL[indexOfDot:]
            if extension != 'jpg' and extension != 'jpeg' and extension != 'png':
                return fail(request) # not a valid image (jpg, jpeg, png)
                
            client_id = '8SkASX_SM8xc-fxMF4SdpzS_b9uew8yG0UrQp0y6'
            secret_id = 'EXkfCNxXeiHtnpsxn9Njui_yUpCuvcSAXzfSYjwN'
                
            clarifai_api = ClarifaiApi(client_id, secret_id) # assumes environment variables are set.
            result = clarifai_api.tag_image_urls(imageURL)
            
            class_list = result['results'][0]['result']['tag']['classes']
            prob_list = result['results'][0]['result']['tag']['probs']
            
            # currently just the list of matched words
            text_output = class_list.__str__()
            
            # Parts of speech recognition
            nouns = []
            verbs = []
            otherPos = []
            story =''
            
            
            image_output = imageURL
            return render(request, 'makestory/output.html',
                {
                'nouns_output': nouns,
                'verbs_output': verbs,
                'otherPos_output': otherPos,
                'imageURL_output': imageURL,
                'story_output': story
                }
            )
        else:
            return index(request)
    return fail(request)
    
def output(request):
    return render(request, 'makestory/output.html')
    
def fail(request):
    return render(request, 'makestory/fail.html')