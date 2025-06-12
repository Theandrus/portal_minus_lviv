from rest_framework import serializers
from .models import MinusstoreMinusauthor


class MinusAuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MinusstoreMinusauthor
        fields = ('name', 'id')
