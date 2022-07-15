from .models import *

# Create your views here.
def model(image_id):
    data = Image.objects.filter(id=image_id) # 학습을 위한 이미지 찾아오기

    result = "sea"
    return result