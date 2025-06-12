from rest_framework import serializers
from minus_lviv.models import DjangoComments


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DjangoComments
        fields = ('comment',)