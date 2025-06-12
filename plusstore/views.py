from django.shortcuts import render
from minusstore.models import MinusstoreMinusplusrecord, MinusstoreMinusrecord

def plusstore_main(request):
    plus = MinusstoreMinusrecord.objects.all()[:20]

    return render(request, 'plusstore/plusstore.html', {
        'plus': plus,
    })
