from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from clarifai.client import ClarifaiApi, ApiError
from PyDictionary import PyDictionary
import nltk
from nltk import pos_tag, CFG
from nltk.parse.generate import generate
import json
from django.contrib import messages
from models import Bigram
import os.path
import sys
import operator
import random
#from libs.en import *

sys.setrecursionlimit(10000)

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
            for i in range(0, len(class_list)/2):
                class_str += class_list[i] + " " 
            
            # currently just the list of matched words
            text_output = class_list.__str__()
            
            # Parts of speech recognition
            tokens = nltk.word_tokenize(class_str)
            # dictionary = PyDictionary()
            
            # nouns = []
            # verbs = []
            # adjectives = []
            # otherPos = []
            # for word in tokens:
            #     #definition = dictionary.meaning(word) # https://pypi.python.org/pypi/PyDictionary/1.3.4
            #     #assignment = definition.keys()[0] # Get the part of speech from the dictonary
            #     assignment = ""
            #     # assignment = tuple[1]
                
            #     if assignment == 'Noun':
            #         nouns.append(word)
            #     elif assignment == 'Verb':
            #         verbs.append(word)
            #     elif assignment == 'Adjective':
            #         adjectives.append(word)
            #     else:
            #         otherPos.append(word)
                    
                    
            # Create the grammar
            #P:prepositions, DET:articles, adverbs
            DET = ["'the'","'a'","'some'"]
            # P = ["'in'","'at'","'since'","'for'","'to'","'past'","'to'""'by'","'in'","'at'","'on'","'under'","'below'","'over'","'above'","'into'","'from'","'of'","'on'","'at'"]
            VB = ["'talks'","'does'","'has'","'cries'", "'fights'", "'traps'", "'bakes'", "'fondles'", "'cooks'", "'sees'", "'calls'", "'smells'", "'tastes'", "'hears'"]
            
            
            assignments = pos_tag(tokens) # tagset='universal' for ADJ, NOUN, etc.
            
            # pos_tags = []
            pos_words = {}
            pos_words['DET'] = DET
            #pos_words['P'] = P
            pos_words['VB'] = VB
            
            for tuple in assignments:
                word = tuple[0]
                pos = tuple[1]
                if pos in pos_words:
                    pos_words[pos].append("\'" + word + "\'")
                else:
                    pos_words[pos] = []
                    pos_words[pos].append("\'" + word + "\'")
                # pos_tags.append(pos)

            #grammar = """
            #S -> NP VP
            #PP -> P NP
            #NP -> Det N
            #VP -> V Det N | V Det N PP
            
            #"""
            
            grammar = """
            S -> NP VP
            NP -> Det N
            VP -> V Det N
            """
            #Det -> 'DT'
            # N -> 'NN'
            # V -> 'VBZ'
            # P -> 'PP'
            
            
            # adverb is RB
            
            if 'DET' in pos_words:
                grammar += 'Det ->' + ' | '.join(pos_words['DET']) + '\n'
                
            if 'P' in pos_words:
                grammar += 'P ->' + ' | '.join(pos_words['P']) + '\n'
                
            if 'NN' in pos_words:
                grammar += 'N ->' + ' | '.join(pos_words['NN']) + '\n'
            #change to VB for nltk
            if 'VB' in pos_words:
                grammar += 'V ->' + ' | '.join(pos_words['VB']) + '\n'
            
            
            #if 'JJ' in pos_words:
            #    grammar += 'A ->' + ' | '.join(pos_words['JJ']) + '\n'
                
            simple_grammar = CFG.fromstring(grammar)
            #  simple_grammar.start()
            # simple_grammar.productions()
            
            sentences = []
            sentence_validity = []
         
            for sentence in generate(simple_grammar, depth=4):
                sentences.append(' '.join(sentence))
            
            
            sentence_validity = get_validity(sentences)
            
            #get_validity(sentences)
            
            # parser = nltk.ChartParser(simple_grammar)
            # tree = parser.parse(pos_tags)
            
            story = ""
            for i in range(0, 10):
                tuple = sentence_validity[i]
                string = tuple[1]
                start_letter = string[0].upper()
                story += start_letter
                story += string[1:]
                story += ". "
            
            caption = 'this is a caption'
            
            return render(request, 'makestory/output.html',
                {
                'imageURL_output': imageURL,
                'caption_output': caption,
                'story_output': story,
                'grammar_test_output': simple_grammar,
                'sentences_test_output': sentences,
                'text_output': sentence_validity,
                }
            )
        else:
            return fail(request)
    return fail(request)
    
    
def get_validity(sentences):
    #bigrams = Bigram.objects.filter(
    #    first_word = "campus",
    #    next_word = "at"
    #)
    #frequency = bigrams[0].frequency
    random.shuffle(sentences)
    sentences = sentences[0:50]
    
    validity = {}
    for sentence in sentences:
        words = sentence.split()
        prev_word_loc = words[0]
        validity[sentence] = 0
        index = 1
        while index < len(words):
            next_word_loc = words[index]
            bigrams = Bigram.objects.filter(
                first_word = prev_word_loc,
                next_word = next_word_loc,
            )
            if len(bigrams) != 0:
                validity[sentence] += bigrams[0].frequency
            
            prev_word_loc = next_word_loc
            index +=   1
    tuple_list = [(v, k) for k, v in validity.iteritems()]
    tuple_list = sorted(tuple_list, key=lambda x: x[0], reverse=True)
    # return validity
    return tuple_list
    
def fail(request):
    return render(request, 'makestory/fail.html')