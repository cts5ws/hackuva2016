from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from clarifai.client import ClarifaiApi
import nltk
from nltk import pos_tag
import json

# Create your views here.
def index(request):
    return render(request, 'makestory/index.html')
    
def output(request):
    # Validation of form
    if request.method == "POST":
        # Validation of request
        if 'inputURL' in request.POST:
            # Validation of image url
            imageURL = request.POST.get('inputURL')
            image_output = imageURL
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
            
            class_str = ""
            for i in range(0, len(class_list)):
                class_str += class_list[i] + " " 
            
            # currently just the list of matched words
            text_output = class_list.__str__()
            
            #Parts of speech recognition
            tokens = nltk.word_tokenize(class_str)
            assignment = pos_tag(tokens)
            nouns = []
            verbs = []
            adjectives = []
            otherPos = []
            for tuple in assignment:
                word = tuple[0]
                assignment = tuple[1]
                if assignment == 'NN' or assignment == 'NNS' or assignment == 'VBG':
                    nouns.append(word)
                elif assignment == 'VBD':
                    verbs.append(word)
                elif assignment == 'JJ':
                    adjectives.append(word)
                else:
                    otherPos.append(word)

            caption = ''
            story = ''
            
            return render(request, 'makestory/output.html',
                {
                'nouns_output': nouns,
                'verbs_output': verbs,
                'adjectives_output': adjectives,
                'otherPos_output': otherPos,
                'imageURL_output': imageURL,
                'caption_output': caption,
                'story_output': story,
                }
            )
        else:
            return fail(request)
    return fail(request)
    
def fail(request):
    return render(request, 'makestory/fail.html')