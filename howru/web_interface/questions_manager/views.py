from django.shortcuts import render

# Create your views here.

def create(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/CREATE)',
    }
    return render(request, 'questions_manager/index.html', context)

def modify(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/MODIFY)',
    }
    return render(request, 'questions_manager/index.html', context)

def delete(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/DELETE)',
    }
    return render(request, 'questions_manager/index.html', context)

def view(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (QUESTIONS MANAGER/VIEW)',
    }
    return render(request, 'questions_manager/index.html', context)