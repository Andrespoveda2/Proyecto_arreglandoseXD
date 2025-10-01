from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_instructor(request):
    # Lógica: Mostrar listado de aprendices y proyectos a supervisar.
    return render(request, 'instructores/dashboard_instructor.html')

@login_required
def proyectos_asignados(request):
    # Lógica: Listado de proyectos que tiene a su cargo.
    return render(request, 'instructores/proyectos_asignados.html')

@login_required
def seguimiento_avance(request, pk):
    # Lógica: Formulario para registrar avances o notas.
    return render(request, 'instructores/seguimiento_avance.html')

