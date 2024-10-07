from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Member
def index(request):
    return HttpResponse("Hello, world!")
def year(request, year):
    return HttpResponse('Year: {}'.format(year))
def age(request, age):
    data = {'age':age}
    return render(request, 'kjapp/age.html', data)
def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('kjapp/all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))