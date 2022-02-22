import os
from django.shortcuts import render, redirect

from .models import Img
from .forms import ImgForm, ImgNonModelForm


def index_test(request):
    imgs = Img.objects.all()
    context = {'imgs': imgs}
    return render(request, 'testapp/index_test.html', context)


def add_img(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index_test')
    else:
        form = ImgForm()
        context = {'form': form}
        return render(request, 'testapp/add_img.html', context)


def add_several_img(request):
    if request.method == 'POST':
        form = ImgNonModelForm(request.POST, request.FILES)
        print('FILES', request.FILES)
        print('=========================================')
        if form.is_valid():
            for file in request.FILES.getlist('img'):
                print('file', round(file.size/1024, 1), 'kB',
                      file.multiple_chunks(chunk_size=100))
                img = Img()
                img.desc = form.cleaned_data['desc']
                img.img = file
                img.save()
            return redirect('index_test')
    else:
        form = ImgNonModelForm()
        context = {'form': form}
        return render(request, 'testapp/add_several_img.html', context)


def get_img(request, pk):
    img = Img.objects.get(pk=pk)
    context = {'img': img}
    return render(request, 'testapp/get_img.html', context)


# Удаление записи из базы данных и отдельно удаляется картинка.
def delete_img(request, pk):
    img = Img.objects.get(pk=pk)
    img.img.delete()
    img.delete()
    return redirect('index_test')