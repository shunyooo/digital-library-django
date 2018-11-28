from django.db.models import Count
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from book.forms import FileFieldForm
from book.models import Book, Tag
from book.tasks import handle_uploaded_file
from django.views.generic.edit import FormView

from django.views.generic import ListView, DetailView

import logging

class HomeView(View):
    def get(self, request, *args, **kwargs):
        # 新着, 適当なタグを探して紐づく本, 10件を10回ぐらいループ
        book_section_list = [
            {"title": "新着アップロード", "list": Book.objects.order_by('-created_at').all()[:10]}
        ]

        # TODO: ここで集計せずbook_countでちゃんと入れておくように
        for tag in Tag.objects.annotate(_book_count=Count('books')).filter(_book_count__gt=0).all()[:10]:
            book_section_list.append({
                "title": tag.content,
                "list": tag.books.all()[:10],
            })

        context = {'book_section_list': book_section_list}
        return render(request, "book/index.html", context=context)


class BookListView(ListView):
    model = Book
    
    template_name = "book/list.html"


class BookDetailView(DetailView):
    model = Book
    template_name = "book/detail.html"


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'book/upload.html'
    success_url = 'upload'

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
