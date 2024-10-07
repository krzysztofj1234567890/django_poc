from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world!")
def year(request, year):
    return HttpResponse('Year: {}'.format(year))
def age(request, age):
    data = {'age':age}
    return render(request, 'kjapp/age.html', data)