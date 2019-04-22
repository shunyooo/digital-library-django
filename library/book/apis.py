import io
import os
import urllib

import requests
from PIL import Image
from rest_framework import viewsets
from rest_framework.response import Response

from .models import WantBook
from .serializers import WantBookSerializer

UPLOAD_DIR = './media/wantbooks/'


def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)


class WantBookViewSet(viewsets.ModelViewSet):
    queryset = WantBook.objects.all()
    serializer_class = WantBookSerializer

    def create(self, request, *args, **kwargs):
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        title = request.POST['title']
        wantbook, created = WantBook.objects.get_or_create(title=title)

        if 'author_name' in request.POST.keys():
            wantbook.author_name = request.POST['author_name']

        print(request.__dict__)
        if 'image' in request.POST.keys():
            url = request.POST['image']
            fn, ext = os.path.splitext(url)
            save_filename = f'{title}{ext}'
            save_path = os.path.join(UPLOAD_DIR, save_filename)
            download_img(url, save_path)
            wantbook.image = save_path

        if 'image' in request.FILES.keys():
            file = request.FILES['image']
            print('image_file', file)
            fn, ext = os.path.splitext(file.name)
            save_filename = f'{title}{ext}'
            save_path = os.path.join(UPLOAD_DIR, save_filename)
            destination = open(save_path, 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            wantbook.image = save_path

        wantbook.save()

        return Response({
            'message': 'OK',
            'wantbook': WantBookSerializer(wantbook).data,
            'created': created,
        })
