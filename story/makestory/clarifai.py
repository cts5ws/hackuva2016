from clarifai.client import ClarifaiApi
import json

def process_picture(url):
    clarifai_api = ClarifaiApi() # assumes environment variables are set.
    result = clarifai_api.tag_image_urls(url)
            
    class_list = result['results'][0]['result']['tag']['classes']
    prob_list = result['results'][0]['result']['tag']['probs']
    
    return class_list.__str__()

