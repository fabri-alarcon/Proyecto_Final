from django.shortcuts import render, HttpResponse, redirect
from .models import Noticia, Categoria, Contacto, Comentario
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  

from .forms import ContactoForm, NoticiaForm
# importamos reverse lazy para los comentarios
from django.urls import reverse_lazy

from django.views.generic.edit import UpdateView, DeleteView

# decorador para ver las noticias solamente como usuario logueado
from django.contrib.auth.decorators import login_required

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


# def add_noticias(request):
#     data = NoticiaForm().save() 
#     # # }
#     # if request.method == 'POST':
#     # NoticiaForm(data=request.POST).save()
     
#     return render(request, 'contacto/formulario.html', {"form": data})

# def editnoticia(LigunRequiredMinxin, UserPassesTestMixin, UpdateView):
#     model = Noticia
#     fields = ["body"]
#     template_name=''


class editnoticia(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Noticia
    fields=['body']
    template_name='templates/noticias/edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('noticias:detalle', kwargs={'pk':pk})

    def test_func(self):
        post = self.get_object()
        return self.request.titulo == post.titulo
    

class deletnoticia(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Noticia
    template_name='templates/noticias/delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.titulo == post.titulo