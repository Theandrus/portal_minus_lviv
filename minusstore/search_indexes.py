from haystack import indexes
from .models import MinusstoreMinuscategory

class MinusCatIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    display_name = indexes.CharField(model_attr='display_name')

    def get_model(self):
        return MinusstoreMinuscategory

    def prepare_name(self, obj):
        return [a.name for a in obj.minusstoreminuscategory_set.all()]

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
