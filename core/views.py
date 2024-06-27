from pyexpat.errors import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from .serializers import *
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
import requests
from django.core.paginator import Paginator






def voucher(request):
    return render(request, 'core/voucher.html') 


#METODO PARA LISTAR DESDE EL API
def artesapi(request):
    response = requests.get('http://127.0.0.1:8000/api/artes/')
    arte = response.json()

    response = requests.get('https://www.mindicador.cl/api/dolar/19-06-2024/')
    data = response.json()

    response2 = requests.get('https://randomuser.me/api/')
    randomuser = response2.json()['results']
    
    
    if 'serie' in data and len(data['serie']) > 0:
        precio = data['serie'][0]['valor']
    else:
        precio = None

    paginator = Paginator(arte, 3) # Muestra 9 cartas por pagina
    page_number = request.GET.get('page') # Busca la pagina
    page_obj = paginator.get_page(page_number)

    aux = {
        'lista' : arte,
        'page_obj' : page_obj,
        'precio' :precio,
        'randomuser' : randomuser,
    }

    return render(request, 'core/crudapi/index.html', aux)


def artesapi(request):
    response = requests.get('http://127.0.0.1:8000/api/artes/')
    arte = response.json

    response = requests.get('https://www.mindicador.cl/api/dolar/19-06-2024/')
    data = response.json()

    response2 = requests.get('https://randomuser.me/api/')
    randomuser = response2.json()['results']
    
    
    if 'serie' in data and len(data['serie']) > 0:
        precio = data['serie'][0]['valor']
    else:
        precio = None

    aux = {
        'arte' :arte,
        'precio' :precio,
        'randomuser' : randomuser,
    }

    return render(request, 'core/crudapi/index.html', aux)




def artedetalle(request, id):
    response = requests.get(f'http://127.0.0.1:8000/api/artes/{id}/')
    arte = response.json

    return render(request, 'core/crudapi/detalle.html', {'arte' : arte})
 


# UTILIZAMOS LAS VIEWSET PARA MANEJAR LAS PETICIONES HTTP (GET,POST,PUT,DELETE)
class TipoArteViewset(viewsets.ModelViewSet):
    queryset = TipoArte.objects.all()
    serializer_class = TipoArteSerializers
    renderer_classes = [JSONRenderer]

class ArteViewset(viewsets.ModelViewSet):
    queryset = Arte.objects.all()
    serializer_class = ArteSerializers
    renderer_classes = [JSONRenderer]



#group required
def user_in_group(user, group_name):
    #$return user.groups.filter(name=group_name).exists() # sin staff
    return user.is_superuser or user.groups.filter(name=group_name).exists() #Con staff includio

def group_required(group_name):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if user_in_group(request.user, group_name):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("No tienes permisos para acceder a esta pagina")
        return _wrapped_view
    return decorator



# Create your views here.




def Edvardmun(request):
    return render(request, 'core/Edvardmun.html')      

def VanGoh(request):
    return render(request, 'core/Vangoh.html')  

def Leonardo(request):
    return render(request, 'core/Leonardo.html')      

def account_locked(request):
    return render(request, 'core/account_locked.html')

def pago(request):
    return render(request,'core/pago.html')

def exitoso(request):
    return render(request,'core/exitoso.html')

#Recorrer productos
@group_required('supervisor')
def solicitudes(request):
    productos = Arte.objects.all()
    aux = {
        'lista' : productos
    }

    return render(request, 'core/solicitudes.html',aux)




#Recorrer productos
@login_required
def listados (request):
    productos = Arte.objects.all()
    aux = {
        'lista' : productos
    }

    return render(request, 'core/detalle_producto.html',aux)


def visualizar(request):
    # Obtener la lista de artes desde la API
    response = requests.get('http://127.0.0.1:8000/api/artes/')
    arte = response.json()

    # Paginación de los artes
    paginator = Paginator(arte, 3)  # Muestra 3 artes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obtener los items del carrito desde la sesión de Django
    carrito = request.session.get('carrito', {})
    items_carrito = []
    total_carrito = 0

    for arte_id, item_data in carrito.items():
        arte_obj = get_object_or_404(Arte, id=int(arte_id))
        subtotal = item_data['cantidad'] * arte_obj.precio
        total_carrito += subtotal
        items_carrito.append({
            'arte': arte_obj,
            'cantidad': item_data['cantidad'],
            'subtotal': subtotal,
        })

    context = {
        'lista': arte,
        'page_obj': page_obj,
        'items_carrito': items_carrito,
        'total_carrito': total_carrito,
    }

    return render(request, 'core/index.html', context)


def agregar_al_carrito(request, arte_id):
    # Obtener el arte con el arte_id proporcionado o devolver un error 404 si no existe
    arte = get_object_or_404(Arte, id=arte_id)
    
    # Obtener la cantidad del formulario o establecerla en 1 por defecto
    cantidad = int(request.POST.get('cantidad', 1))

    # Obtener el carrito actual de la sesión de Django
    carrito = request.session.get('carrito', {})

    # Convertir arte_id a string para usarlo como clave en el diccionario
    arte_id_str = str(arte_id)

    # Verificar si el arte_id ya está en el carrito
    if arte_id_str in carrito:
        # Sumar la cantidad del formulario a la cantidad existente en el carrito
        carrito[arte_id_str]['cantidad'] += cantidad
    else:
        # Agregar un nuevo elemento al carrito con la cantidad inicial del formulario
        carrito[arte_id_str] = {'cantidad': cantidad}

    # Actualizar la sesión de carrito con el nuevo valor
    request.session['carrito'] = carrito

    return redirect('index')

def vaciar_carrito(request):
    if request.method == 'POST':
        # Vaciar el carrito de la sesión
        request.session['carrito'] = {}
    return redirect('index')  # Redirige a la página principal o la página que desees

#CRUD
@login_required
def arteadd(request):
    aux = {
        'form': ArteForm()
    }

    if request.method == "POST":
        formulario = ArteForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            #aux['msj'] = "Producto agregado correctamente."
            return redirect('producto')  
        else:
            aux['form'] = formulario
            #aux['msj'] = "El Producto no fue agregado."

    return render(request,'core/crud/add.html',aux)
    


@login_required
def arteupdate(request, id):
    producto = Arte.objects.get(id=id)
    aux = {
        'form': ArteForm(instance=producto)
    }

    if request.method == "POST":
        formulario = ArteForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            # Cambiar el estado del producto a 'pendiente'
            producto.estado = 'pendiente'
            producto.save()
            aux['form'] = formulario
            #aux['msj'] = "Producto modificado correctamente."
            return redirect('producto')  
        else:
            aux['form'] = formulario
            #aux['msj'] = "El Producto no fue modificado."

    return render(request, 'core/crud/update.html', aux)



@login_required
def artedelete(request,id):
    producto = Arte.objects.get(id=id)
    producto.delete()

    return redirect("producto")




@login_required
def aceptado(request, id):
    # Obtener el producto de Arte por su ID
    producto = Arte.objects.get(id=id)

    # Cambiar el estado del producto a 'aceptado'
    producto.estado = 'aceptado'
    producto.save()
    
    # Crear una instancia del formulario ArteForm con el producto actualizado
    form = ArteForm(instance=producto)
    
    # Pasar el formulario al contexto de la plantilla
    context = {
        'form': ArteForm(instance=producto)
    }
    return redirect('solicitudes')
   
@login_required
def rechazado(request, id):
    # Obtener el producto de Arte por su ID
    producto = Arte.objects.get(id=id)

    # Cambiar el estado del producto a 'aceptado'
    producto.estado = 'rechazado'
    producto.save()
    
    # Crear una instancia del formulario ArteForm con el producto actualizado
    form = ArteForm(instance=producto)
    
    # Pasar el formulario al contexto de la plantilla
    context = {
        'form': ArteForm(instance=producto)
    }
    return redirect('solicitudes')



#Register
def register(request):
    aux = {
        'form': CustomUserCreationForm()
    }

    if request.method == "POST":
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            group = Group.objects.get(name='cliente')
            user.groups.add(group)

            return redirect("index")
        else:
            aux['form'] = formulario

    return render(request, 'registration/register.html', aux)

