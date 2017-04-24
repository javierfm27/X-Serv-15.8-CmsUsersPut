from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from cms_users_put.models import Pages


# Create your views here.
@csrf_exempt
def barra(request):
    if request.user.is_authenticated():
        htmlAnswer = "Logged in as " + request.user.username \
            + ". <a href='/logout'> Logout </a>"
        if request.method == 'GET':
            htmlAnswer = htmlAnswer + "<form id='paginas' method='POST'>" \
                    + "<label> Introduce el recurso y el contenido del recurso" \
                    + "</br></label>" \
                    + "<input name='name' type='text'>" \
                    + "<br>" \
                    + "<textarea name='page' rows='20' cols='100' ></textarea>" \
                    + "<br>" \
                    + "<input type='submit' value='Enviar'></form>"
            listaPages = Pages.objects.all()
            htmlAnswer = htmlAnswer + "Paginas Disponibles:<br>"
            for pagina in listaPages:
                htmlAnswer = htmlAnswer + "<a href='/" + pagina.nombre \
                    + "'> Pagina de " + pagina.nombre + "</a><br>"
            return HttpResponse(htmlAnswer)
        elif request.method == 'POST':
            recurso = request.POST['name']
            contenido = request.POST['page']
            pagina = Pages(nombre=recurso, pagina=contenido)
            pagina.save()
            return HttpResponse("Hacemos un POST en /" + recurso)
    else:
        response = HttpResponse()
        response.write("No Estas Logeado para Crear Paginas " \
            + "<a href='/admin/'> Login </a><br> " \
            + "Pero puedes echar un vistazo a nuestras paginas: <br>")
        listaPages = Pages.objects.all()
        for pagina in listaPages:
            response.write("<a href='/" + pagina.nombre + "'> Pagina de " + pagina.nombre + "</a><br>")
        return response

@csrf_exempt
def processRec(request, nombreRecurso):
    if request.method == "GET":
        if request.user.is_authenticated():
            htmlAnswer = "Logged in as " + request.user.username \
                + ". <a href='/logout'> Logout </a><br>"
        else:
            htmlAnswer = "No Estas Logeado para Crear Paginas " \
            + "<a href='/admin/'> Login </a><br> "
        try:
            pagina = Pages.objects.get(nombre=nombreRecurso)
            htmlAnswer = htmlAnswer + pagina.pagina
            return HttpResponse(htmlAnswer)
        except Pages.DoesNotExist:
            return HttpResponseNotFound(htmlAnswer + "Page Not Found")
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            try:
                pagina = Pages.objects.get(name=nombreRecurso)
                pagina.page = request.body.decode('utf-8')
                pagina.save()
                return(HttpResponse("Se ha actualizado /" + nombreRecurso))
            except Pages.DoesNotExist:
                return HttpResponseNotFound("ERROR! Realizando un PUT sobre algo inexistente")
        else:
            return HttpResponseBadRequest("ERROR! NO PUEDES REALIZAR ESTA OPERACION")

def mylogout(request):
    logout(request)
    return redirect(barra)
