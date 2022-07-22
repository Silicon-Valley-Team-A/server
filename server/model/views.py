from .models import *
import PIL
import clip
import torch
import csv
import urllib

# Create your views here.

def model(image_id):
    f = open('./model/keywords.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    text = []
    for line in rdr:
        text.append(line[0])
    f.close()


    ## Model

    # Load the model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load('ViT-B/32', device)

    ## Zero-shot Prediction

    # Prepare the inputs
    data = Image.objects.get(id=image_id) # 학습을 위한 이미지 찾아오기
    image_url = "." + urllib.parse.unquote(data.image.url)
    image = PIL.Image.open(image_url)
    image_input = preprocess(image).unsqueeze(0).to(device)
    text_inputs = torch.cat([clip.tokenize(f"a photo of a {c}") for c in text]).to(device)

    # Calculate features
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_inputs)

    # Pick the top 5 most similar labels for the image
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    print(100.0 * image_features @ text_features.T)

    values, indices = similarity[0].topk(5)


    # Print the result
    print("\nTop predictions:\n")
    n = 0
    for value, index in zip(values, indices):
        if n==0:
            keyword = text[index]
        n= n+1
        print(f"{text[index]:>16s}: {100 * value.item():.2f}%%")

    print(keyword)
    return keyword