from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from clarifai.client import ClarifaiApi, ApiError
import nltk
from PyDictionary import PyDictionary
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
            try:
                result = clarifai_api.tag_image_urls(imageURL)
            except ApiError:
                #return fail(request)
                
                message = _("ApiError")
                request.user.message_set.create(message = message)
                
                return redirect('fail.html')
            
            
            class_list = result['results'][0]['result']['tag']['classes']
            prob_list = result['results'][0]['result']['tag']['probs']
            
            class_str = ""
            for i in range(0, len(class_list)):
                class_str += class_list[i] + " " 
            
            # currently just the list of matched words
            text_output = class_list.__str__()
            
            # Parts of speech recognition
            tokens = nltk.word_tokenize(class_str)
            dictionary = PyDictionary()
            
            
            #assignment = pos_tag(tokens, tagset='universal') # universal gives us 'ADJ', 'NOUN', etc.
            nouns = []
            verbs = []
            adjectives = []
            otherPos = []
            for word in tokens:
                definition = dictionary.meaning(word) # https://pypi.python.org/pypi/PyDictionary/1.3.4
                assignment = definition.keys()[0] # Get the part of speech from the dictonary
                
                # assignment = tuple[1]
                
                if assignment == 'Noun':
                    nouns.append(word)
                elif assignment == 'Verb':
                    verbs.append(word)
                elif assignment == 'Adjective':
                    adjectives.append(word)
                else:
                    otherPos.append(word)

            caption = 'this is a caption'
            story = 'this is the story'
            
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