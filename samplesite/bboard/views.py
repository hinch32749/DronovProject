from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, ListView, FormView, UpdateView, DeleteView

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

# ======================================================================================
#  Класс для детального вывода Объявления.

class BbDetailView(DetailView):
    """Выводит описание выбранного объявления."""
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# ==================================================================================
# Классы для вывода Рубрики с ее объявлениями.

class BbByRubricView(ListView):
    """Выводит выбранную рубрику и все ее объявления."""
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


# class BbByRubricView(TemplateView):
#     """Выводит выбранную рубрику и все ее объявления."""
#     template_name = 'bboard/by_rubric.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.all()
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         return context


# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
#     return render(request, 'bboard/by_rubric.html', context)
# =====================================================================================
# Класс для удаления Объвлений.

class BbDeleteView(DeleteView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def get_success_url(self):
        return reverse('by_rubric', kwargs={'rubric_id': self.object.rubric.id})

# =====================================================================================
# Класс для редактирования Объявлений.

class BbEditView(UpdateView):
    """Класс позволяющий исправлять Объявления."""
    model = Bb
    form_class = BbForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def get_success_url(self):
        return reverse('detail',
                       kwargs={'pk': self.object.id})


# =====================================================================================
# Классы для работы с формами и добавлением новый объявлений.

class BbAddView(FormView):
    """Класс добавления нового Объявления."""
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


# class BbCreateView(CreateView):
#     """Создание нового объявления."""
#     template_name = 'bboard/create.html'
#     form_class = BbForm
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context
# ====================================================================================

def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)
