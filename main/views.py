import genericpath
from django.shortcuts import render

# Create your views here.
class IndexView(genericpath.ListView):
    template_name = "main/index.html"
    
def matches(request):
    return render(request)

def table(request):
    return render(request)

def statistics(request):
    return render(request)

def club(request):
    return render(request)

def player(request):
    return render(request)