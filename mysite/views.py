"""
Views page for the home/defaul page that opens when you click on
the server
"""
from django.shortcuts import render
from django.http import HttpResponse

def home(*args, **kwargs):
    return HttpResponse("<h1>Home Page</h1>")
