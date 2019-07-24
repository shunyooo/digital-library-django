import json

from django.db.models import Count
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from book.forms import FileFieldForm
from book.models import Book, Tag, WantBook
from book.tasks import handle_uploaded_file
from django.views.generic.edit import FormView, UpdateView, DeleteView

from django.views.generic import ListView, DetailView

import logging


def _get_tag_context():
    # TODO: Mixinにする
    tag_list = Tag.objects.filter(book_count__gt=0)
    return {
        'tag_list': tag_list,
        'tag_list_str': ','.join([tag.content for tag in tag_list]),
    }


class HomeView(View):
    def get(self, request, *args, **kwargs):
        # 新着, 適当なタグを探して紐づく本, 10件を10回ぐらいループ
        section_list = [
            {"section_type": "book_list", "section_title": "Recent Upload",
             "section_sub_title": "最近アップロードされた本たち",
             "book_list": Book.objects.order_by('-created_at').all()[:10], "book_key": "new", },
            {"section_type": "tag_list", "section_title": "Tag", "section_sub_title": "タグから本を探そう",
             "tag_list": Tag.objects.filter(book_count__gt=0),
             "bg_color": 'bg-brown',
             },
        ]

        # タグ付き本のピックアップ
        valid_tag_q = Tag.objects.annotate(_book_count=Count('books')).filter(_book_count__gt=0).order_by('?')[:3]
        for i, tag in enumerate(valid_tag_q):
            section_list.append({
                "section_type": "book_list",
                "section_title": f"Pickup Books {i+1}",
                "section_sub_title": f"{tag.content}のタグが付いている本たち",
                "book_list": tag.books.all()[:10],
                "book_key": "tag",
                "tag_key": tag.content,
                'border_bottom': 'border-brown',
            })

        context = {'section_list': section_list}
        context.update(_get_tag_context())
        return render(request, "book/index.html", context=context)


class WantBookListView(ListView):
    model = WantBook
    context_object_name = "want_book_list"
    template_name = "book/want_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WantBookListView, self).get_context_data(**kwargs)
        context.update(_get_tag_context())
        print(context)
        return context


class BookListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "book/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context.update(_get_tag_context())

        # meta タイトル用
        search_key = ''
        for key in ['title', 'tag', 'author']:
            value_list = self.request.GET.getlist(key)
            search_key += ' '.join(value_list)

        context.update({'search_key': search_key})
        print('get_context_data!!!!')
        print(context)
        return context

    def get_queryset(self):
        # TODO: タイトル, タグ, 著者で検索
        result_qs = self.model.objects.all()

        # AND検索
        # タイトル
        q_title_list = self.request.GET.getlist("title")
        for q in q_title_list:
            result_qs = result_qs.filter(title__icontains=q)

        # タグ
        q_tag_list = self.request.GET.getlist("tag")
        for q in q_tag_list:
            result_qs = result_qs.filter(tag__content=q)

        # 著者
        q_author_list = self.request.GET.getlist("author")
        for q in q_author_list:
            result_qs = result_qs.filter(author__name__icontains=q)

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
    fields = ('isbn', 'title', 'sub_title', 'description',)
    template_name = "book/update.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookUpdateView, self).get_context_data(**kwargs)
        context.update(_get_tag_context())
        context['book_tag_list_str'] = ','.join(context['book'].tag.values_list('content', flat=True))
        return context

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        tag_list = request.POST['tags-edit-input'].split(' ')
        tag_list = [tag for tag in tag_list if tag != '']
        book = self.object

        logging.debug(f'post:{tag_list}')
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

    def get_form(self, form_class=None):
        form = super(BookUpdateView, self).get_form(form_class)
        form.fields['sub_title'].required = False
        form.fields['description'].required = False
        form.fields['isbn'].required = False
        return form


class BookDeleteView(DeleteView):
    model = Book
    template_name = "book/confirm_delete.html";
    success_url = reverse_lazy('book:index')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
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
