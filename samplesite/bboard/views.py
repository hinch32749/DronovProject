
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView

from .models import Bb, Rubric
from .forms import BbForm

# ========================================================================================================
# Всякие примеры из книги


# Потоковый ответ представляется классом StreamingHttpResponse.
# def index(request):
#     bbs = Bb.objects.all()
#     resp = StreamingHttpResponse(bbs,
#                                  content_type='text/plain; charset=utf-8')
#     return resp


# Для отправки клиентам файлов применяется класс FileResponse
# Отправка картинки Джафара:)
# from django.http import FileResponse
# def index(request):
#     filename = r'd:/jafar.png'
#     return FileResponse(open(filename, 'rb'))


# Для отправки данных в формате JSON применяется класс JsonResponse
# from django.http import JsonResponse
# from django.core.serializers.json import DjangoJSONEncoder
# def index(request):
#     data = {'title': 'Bicycle', 'content': 'Old', 'price': 10000.0}
#     return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)

# ========================================================================================================
class BbDetailView(DetailView):
    """Выводит описание выбранного объявления."""
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


class BbByRubricView(TemplateView):
    """Выводит выбранную рубрику и все ее объявления."""
    template_name = 'bboard/by_rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context


# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
#     return render(request, 'bboard/by_rubric.html', context)


class BbCreateView(CreateView):
    """Создание нового объявления."""
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)
