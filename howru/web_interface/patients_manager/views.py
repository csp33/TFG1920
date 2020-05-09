from django.shortcuts import render

# Create your views here.

def assign(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (PATIENTS MANAGER/ASSIGN)',
    }
    return render(request, 'patients_manager/assign.html', context)

def unassign(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (PATIENTS MANAGER/UNASSIGN)',
    }
    return render(request, 'patients_manager/unassign.html', context)

def view(request):
    context = {
        'test_var': 'TEST VARIABLE THAT COMES FROM PYTHON CODE (PATIENTS MANAGER/VIEW)',
    }
    return render(request, 'patients_manager/view.html', context)