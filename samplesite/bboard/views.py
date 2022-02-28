from django.forms import modelformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.http import StreamingHttpResponse, HttpRequest
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, ListView, FormView, \
    UpdateView, DeleteView, ArchiveIndexView, DateDetailView, RedirectView

from .models import Bb, Rubric
from .forms import BbForm, RubricBaseFormSet, SearchForm

from django.db.models.signals import post_save

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


# class BbDetailView(DateDetailView):
#     """Выводит описание выбранного объявления."""
#     model = Bb
#     date_field = 'published'
#     month_format = '%m'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context
#
#
# class BbRedirectView(RedirectView):
#     url = '/detail/%(pk)d/'


# ==================================================================================
# Классы для вывода Рубрики с ее объявлениями.
# Листинг 10.12 Дронова представляет еще один вариант контроллеров смешанной функциональности.
# Но советует его не использовать. Для примера смотри Листинг 10.12.

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
# Класс выводящий Объявления по дате и функция выводящяя главную страницу.

# class BbIndexView(ArchiveIndexView):
#     model =Bb
#     date_field = 'published'
#     date_list_period = 'year'
#     template_name = 'bboard/index.html'
#     context_object_name = 'bbs'
#     allow_empty = True
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context
#

def index(request):
    bbs = Bb.objects.all()
    # rubrics = Rubric.objects.all()
    print(request.COOKIES)
    print(request.get_signed_cookie(key='sessionid', salt='SECRET_KEY'))
    if 'counter' in request.COOKIES:
        request.COOKIES['counter'] += 1
        print(True)
    else:
        print(False)
        request.COOKIES['counter'] = 1

    paginator = Paginator(bbs, 4)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'bbs': page.object_list, 'page': page}
    # print(request.GET)
    return render(request, 'bboard/index.html', context)


# ====================================================================================
# Класс для удаления Объвлений.

class BbDeleteView(DeleteView):
    model = Bb
    template_name = 'bboard/bb_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def get_success_url(self):
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.rubric.id})


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
        return reverse('bboard:detail',
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
        return reverse('bboard:by_rubric',
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
#
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_order=True, can_delete=True,
                                         formset=RubricBaseFormSet)
    rubric = Rubric.objects.all()
    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.save()
            return redirect('bboard:index')
    else:
        formset = RubricFormSet()
    context = {'formset': formset, 'rubrics': rubric}
    return render(request, 'bboard/rubrics.html', context)


# Контроллер, который использует форму не связанную с моделями, для поиска рубрики.
def search(request):
    rubrics = Rubric.objects.all()
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        try:
            if sf.is_valid():
                print('here', sf.errors)
                keyword = sf.cleaned_data['keyword'].title()
                rubric_id = sf.cleaned_data['rubric'].pk
                bbs = Bb.objects.filter(title__icontains=keyword, rubric=rubric_id)
                if bbs:
                    context = {'bbs': bbs, 'rubrics': rubrics}
                    return render(request, 'bboard/search_result.html', context)
                else:
                    sf = SearchForm()
                    context = {'form': sf, 'rubrics': rubrics}
                    return render(request, 'bboard/search.html', context)
        except Exception as ex:
            sf = SearchForm()
            context = {'form': sf, 'rubrics': rubrics, 'ex': ex}
            return render(request, 'bboard/search.html', context)
    else:
        sf = SearchForm()
    context = {'form': sf, 'rubrics': rubrics}
    return render(request, 'bboard/search.html', context)

