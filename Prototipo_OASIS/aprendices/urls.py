from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_aprendiz(request):
    # Lógica: Mostrar sus proyectos asignados y pendientes.
    return render(request, 'aprendices/dashboard_aprendiz.html')

@login_required
def proyectos_disponibles(request):
    # Lógica: Mostrar proyectos filtrados por su programa.
    return render(request, 'aprendices/proyectos_disponibles.html')

@login_required
def detalle_proyecto(request, pk):
    # Lógica: Mostrar detalles de un proyecto.
    return render(request, 'aprendices/detalle_proyecto.html')

@login_required
def asignacion_list(request):
    # Lógica: Listado de proyectos en los que se postuló/fue asignado.
    return render(request, 'aprendices/asignacion_list.html')