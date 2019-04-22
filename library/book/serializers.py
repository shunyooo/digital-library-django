from rest_framework import serializers
from .models import WantBook

class WantBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantBook
        fields = ('title', 'image', 'author_name')