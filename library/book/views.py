import json

from django.db.models import Count
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from book.forms import FileFieldForm
from book.models import Book, Tag
from book.tasks import handle_uploaded_file
from django.views.generic.edit import FormView, UpdateView

from django.views.generic import ListView, DetailView

import logging


def _get_tag_context():
    # TODO: Mixinにする
    tag_list = Tag.objects.all()
    return {
        'tag_list': tag_list,
        'tag_list_str': ','.join([tag.content for tag in tag_list]),
    }


class HomeView(View):
    def get(self, request, *args, **kwargs):
        # 新着, 適当なタグを探して紐づく本, 10件を10回ぐらいループ
        book_section_list = [
            {"title": "新着アップロード", "list": Book.objects.order_by('-created_at').all()[:10], "key": "new"}
        ]

        # TODO: ここで集計せずbook_countでちゃんと入れておくように
        for tag in Tag.objects.annotate(_book_count=Count('books')).filter(_book_count__gt=0).all()[:10]:
            book_section_list.append({
                "title": tag.content,
                "list": tag.books.all()[:10],
                "key": "tag",
            })

        context = {'book_section_list': book_section_list}
        context.update(_get_tag_context())
        return render(request, "book/index.html", context=context)


class BookListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "book/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context.update(_get_tag_context())
        return context

    def get_queryset(self):
        # TODO: タイトル, タグ, 著者で検索
        result_qs = self.model.objects.all()

        # AND検索
        # タイトル
        q_title_list = self.request.GET.getlist("title")
        for q in q_title_list:
            result_qs = result_qs.filter(title__contains=q)

        # タグ
        q_tag_list = self.request.GET.getlist("tag")
        for q in q_tag_list:
            result_qs = result_qs.filter(tag__content=q)

        # 著者
        q_author_list = self.request.GET.getlist("author")
        for q in q_author_list:
            result_qs = result_qs.filter(author__name__contains=q)

        logging.debug(result_qs.query)

        return result_qs


class BookDetailView(DetailView):
    model = Book
    template_name = "book/detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context.update(_get_tag_context())
        context['book_tag_list_str'] = ','.join(context['book'].tag.values_list('content', flat=True))
        return context


class BookUpdateView(UpdateView):
    model = Book
    fields = ('title',)
    template_name = "book/update.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookUpdateView, self).get_context_data(**kwargs)
        context.update(_get_tag_context())
        context['book_tag_list_str'] = ','.join(context['book'].tag.values_list('content', flat=True))
        return context

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        tag_list = request.POST['tags-edit-input'].split(' ')
        book = self.object

        # remove
        for old_tag_obj in book.tag.all():
            if old_tag_obj.content not in tag_list:
                book.tag.remove(old_tag_obj)

        # add
        old_tag_list = book.tag.all().values_list('content', flat=True)
        add_tag_list = [_tag for _tag in tag_list if _tag not in old_tag_list]
        for _tag in add_tag_list:
            tag_obj, is_create = Tag.objects.get_or_create(content=_tag)
            book.tag.add(tag_obj)

        return result

    def form_valid(self, form):
        result = super().form_valid(form)
        print(form)
        print('form_valid!! ', result)
        return result


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'book/upload.html'
    success_url = 'upload'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FileFieldView, self).get_context_data(**kwargs)
        context.update(_get_tag_context())
        return context

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        logging.debug(request.FILES)
        file_list = request.FILES.getlist('file')
        if form.is_valid():
            for f in file_list:
                try:
                    handle_uploaded_file(f)
                except Exception as e:
                    return HttpResponseServerError(e.args)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
