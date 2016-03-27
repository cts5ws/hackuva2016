from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from clarifai.client import ClarifaiApi, ApiError
from PyDictionary import PyDictionary
import nltk
from nltk import pos_tag, CFG
from nltk.parse.generate import generate
import json
from django.contrib import messages

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
                
                messages.add_message(request, messages.INFO, "ApiError")
                return HttpResponseRedirect('makestory/fail.html')
            
            
            class_list = result['results'][0]['result']['tag']['classes']
            prob_list = result['results'][0]['result']['tag']['probs']
            
            class_str = ""
            for i in range(0, len(class_list)):
                class_str += class_list[i] + " " 
                    nouns
            # currently just the list of matched words
            text_output = class_list.__str__()
            
            # Parts of speech recognition
            tokens = nltk.word_tokenize(class_str)
            dictionary = PyDictionary()
            
            
            
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
                    
                    
            # Create the grammar
            #P:prepositions, DET:articles, adverbs
            P = ["on","in","at","since","for","ago","before","to","past","to","until","by","in","at","on","under","below","over","above","into","from","of","on","at"]
            DET = ["the","a","one","some","few","a few","the few","some"]
            
            assignments = pos_tag(tokens) # tagset='universal' for ADJ, NOUN, etc.
            
            pos_tags = []
            pos_words = {}
            for tuple in assignments:
                word = tuple[0]
                pos = tuple[1]
                if pos in pos_words:
                    pos_words[pos].append(word)
                else:
                    pos_words[pos] = []
                pos_tags.append(pos)
                
                
            
            
            grammar = """
            S -> NP VP
            PP -> P NP
            NP -> Det N | Det N PP
            VP -> V NP | VP PP
            Det -> 'DT'
            """
            # N -> 'NN'
            # V -> 'VBZ'
            # P -> 'PP'
            
            
            # adverb is RB
            
            if 'NN' in pos_words:
                grammar += 'N ->' + ' | '.join(pos_words['NN']) + '\n'
            
            if 'VB' in pos_words:
                grammar += 'V ->' + ' | '.join(pos_words['VB']) + '\n'
                
            if 'JJ' in pos_words:
                grammar += 'A ->' + ' | '.join(pos_words['JJ']) + '\n'
                
            simple_grammar = CFG.fromstring(grammar)
            #simple_grammar.start()
            simple_grammar.productions()
            
            sentences = []
            for sentence in generate(simple_grammar, n=10):
                sentences.append(' '.join(sentence))
            
            # parser = nltk.ChartParser(simple_grammar)
            # tree = parser.parse(pos_tags)
            


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
                'sentences_test_output': sentences,
                }
            )
        else:
            return fail(request)
    return fail(request)
    
def fail(request):
    return render(request, 'makestory/fail.html')