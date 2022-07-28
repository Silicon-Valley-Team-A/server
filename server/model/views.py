from .models import *
import PIL
import clip
import torch
import csv
import numpy as np
import urllib.request
import tensorflow as tf 

# Create your views here.
def model(image_id):
    f = open('./model/keywords.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    text = []
    change = []
    for line in rdr:
        text.append(line[0])
        change.append(line[1])
    f.close()

    result = {}

    ### Keyword model ###
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load('ViT-B/32', device)


    ### Prepare the inputs ###
    data = Image.objects.get(id=image_id)
    image_url = "." + urllib.parse.unquote(data.image.url)
    image = PIL.Image.open(image_url)
    image_input = preprocess(image).unsqueeze(0).to(device)
    text_inputs = torch.cat([clip.tokenize(f"a photo of a {c}") for c in text]).to(device)


    ### mood model ###
    classes = ("happy", "sad", "scary")
    mood_model_keras = tf.keras.models.load_model('./model/moodmodel_keras_2.h5')
    print("keras: "+classes[np.argmax(mood_model_keras(np.expand_dims(np.array(image.resize((192,192))), axis=0)).numpy())])
    result['mood'] = classes[np.argmax(mood_model_keras(np.expand_dims(np.array(image.resize((192,192))), axis=0)).numpy())]


    # Calculate features
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_inputs)

    # Pick the top 5 most similar labels for the image
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
    values, indices = similarity[0].topk(5)


    # Print the result
    print("\nTop predictions:\n")
    n = 0
    keyword = []
    for value, index in zip(values, indices):
    
        keyword.append(text[index])
        
        n= n+1
        print(f"{text[index]:>16s}: {100 * value.item():.2f}%%")

    print(keyword)
    result['keyword'] = keyword
    return result