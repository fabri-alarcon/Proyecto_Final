from django.shortcuts import render, HttpResponse, redirect
from .models import Noticia, Categoria, Contacto, Comentario
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  

from .forms import ContactoForm, NoticiaForm
# importamos reverse lazy para los comentarios
from django.urls import reverse_lazy


# decorador para ver las noticias solamente como usuario logueado
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


# uso de decorador para verificar logeo de usuario y poder ver noticia
@login_required
def inicio(request):
    # obtener todas las noticias y mostrar en el inicio.html
    # ctx = {}
    # # clase.objetcs.all()==> select * from noticia
    # noticia = Noticia.objects.all()
    # ctx["noticias"] = noticia
    # return render(request, 'noticias/inicio.html', ctx)
    contexto = {}
    id_categoria = request.GET.get('id', None)

    if id_categoria:
        n = Noticia.objects.filter(categoria_noticia=id_categoria)
    else:
        n = Noticia.objects.all()  # una lista

    contexto['noticias'] = n

    cat = Categoria.objects.all().order_by('nombre')
    contexto['categorias'] = cat

    return render(request, 'noticias/inicio.html', contexto)


@login_required
def Detalle_Noticias(request, pk):
    contexto = {}

    n = Noticia.objects.get(pk=pk)
    contexto['noticia'] = n

   

    c = Comentario.objects.filter(noticia=n)
    contexto['comentarios'] = c

    return render(request, 'noticias/detalle.html', contexto)


# ClaseName.objects.all()[0:2]              select * from noticias
# ClaseName.objects.get(pk = 1)        select * from noticias where id = 1
# ClaseName.objects.filter(categoria)  select * from noticias where categoria = deportes


def contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
           ContactoForm(data=request.POST).save()

    return render(request, 'contacto/formulario.html', data)


@login_required
def Comentar_Noticia(request):
    comentario = request.POST.get('comentario', None)
    user = request.user
    noti = request.POST.get('id_noticia', None)
    noticia = Noticia.objects.get(pk=noti)
    coment = Comentario.objects.create(
        usuario=user, noticia=noticia, texto=comentario)
    return redirect(reverse_lazy('noticias:detalle', kwargs={"pk": noti}))


# creando las clases que me permiten modificar y elimiar los comentarios
class Editcomentario(View):
    def get(self, request, pk):
        comment = Comentario.objects.get(pk=pk) # extraemos el objeto de comentarios con igual pk
        return render(request, 'noticias/edit.html', {'comment': comment})

    def post(self, request, pk):
        comment = Comentario.objects.get(pk=pk)
        nuevo_contenido = request.POST.get('texto')
        comment.texto = nuevo_contenido
        comment.save()
        noticia = comment.noticia      # buscamos de que noticia es el comentario para sarlo para redireccionarme a la misma despues de editarla
        return redirect('noticias:detalle', pk=noticia.pk)



class CommentDeleteView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk) # comprobamos si el usuaro que va a borrarlo es el mismo que quien creó el comentario, para mandarlo al html de delete
        if comment.usuario == request.user:
            return render(request, 'noticias/delete.html', {'comment': comment})
        else:
            noticia = comment.noticia  # sinó lo redireccionamos de nuevo
            return redirect('noticias:detalle', pk=noticia.pk) 

    def post(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk)
        if comment.usuario == request.user: # si el usuario es el que creó el comentario este se borra
            comment.delete()
        noticia = comment.noticia
        return redirect('noticias:detalle', pk=noticia.pk)  


def agregar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('noticias:inicio')
    else:
        form = NoticiaForm()

    return render(request, 'noticias/formulario.html', {'form': form})
  



def eliminar_noticia(request, pk):
    noticia = Noticia.objects.get(pk =pk)
    noticia.delete()
    return redirect("noticias:inicio")




