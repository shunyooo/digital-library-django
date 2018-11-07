from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from book.forms import FileFieldForm
from book.models import Book
from book.tasks import handle_uploaded_file
from django.views.generic.edit import FormView


def index(request):
    return HttpResponse("Hello, world. You're at the book index.")


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book/detail.html', {'book': book})


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'book/upload.html'
    success_url = 'upload'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file_list = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in file_list:
                handle_uploaded_file(f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
