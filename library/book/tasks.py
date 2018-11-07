from collections import namedtuple

from book.models import Author, Category, Book
import os.path


# from utils.pdf import PDFConverter

def handle_uploaded_file(f, author_name=None, category=None):
    """
    file（PDF）をmediaに保存。
    modelにBookを追加し、jpegに分割して保存。
    """
    try:
        # ファイル保存
        save_path = f'./media/{f.name}'
        with open(save_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        # ファイル情報取得
        pdf_info = extract_pdf_file_info(save_path)

        # DB登録
        # TODO: カテゴリもフォーム時点で選べるように
        # _category = None
        # if category:
        #     _category, _ = Category.objects.get_or_create(content=category)

        _book = Book.objects.create(title=pdf_info.title,
                                    page_count=pdf_info.page_count,)

        if author_name:
            _author, _ = Author.objects.get_or_create(name=author_name)
            _book.author.set([_author])

        # TODO: APIより書籍情報を集める

    except Exception as e:
        import traceback
        traceback.print_exc()


PdfInfo = namedtuple('PdfInfo', ('title', 'page_count'))


def extract_pdf_file_info(path):
    title = extract_pdf_title(path)
    return PdfInfo(title=title, page_count=0)


def extract_pdf_title(path):
    filename = os.path.basename(path)
    title, _ = os.path.splitext(filename)
    return title
