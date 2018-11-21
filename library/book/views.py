from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from book.forms import FileFieldForm
from book.models import Book
from book.tasks import handle_uploaded_file
from django.views.generic.edit import FormView

from django.views.generic import ListView, DetailView

import logging


class BookListView(ListView):
    model = Book
    template_name = "book/index.html"

class BookDetailView(DetailView):
    model = Book
    template_name = "book/detail.html"

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book/detail.html', {'book': book})


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
