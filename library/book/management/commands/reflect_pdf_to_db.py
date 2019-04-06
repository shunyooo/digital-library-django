from django.core.management.base import BaseCommand

from book.models import Book
from ...tasks import handle_uploaded_file
import os


class Command(BaseCommand):
    help = 'Reflect Existing PDF to DB'

    def add_arguments(self, parser):
        parser.add_argument('pdf', nargs='+', type=str)

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        pdf_path_list = []
        for pdf in options['pdf']:
            for file_path in files(pdf, only_ext_list=['.pdf']):
                pdf_path_list.append(file_path)

        pdf_title_list = [extract_title(path) for path in pdf_path_list]
        exist_pdf_title_list = list(Book.objects.filter(title__in=pdf_title_list).values_list('title', flat=True))
        exist_index_list = [pdf_title_list.index(title) for title in exist_pdf_title_list]
        dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes]
        target_pdf_path_list = dellist(pdf_path_list, exist_index_list)

        njoin = lambda _list: '\n'.join(_list)
        print(f"""
【登録済み】\n{njoin([path for path in pdf_path_list if path not in target_pdf_path_list])}

【未登録】\n{njoin(target_pdf_path_list)}
        """)

        print(f'{len(pdf_path_list)}件のPDFが見つかりました。\n内{len(target_pdf_path_list)}件が未登録です。\nDBに登録しますか？')
        yn_input = input('y/n: ')
        if 'n' in yn_input.lower():
            print('cancel')
            return

        pdf_count = len(target_pdf_path_list)
        for i, pdf_path in enumerate(target_pdf_path_list):
            with open(pdf_path, 'r') as f:
                print(f'[{i+1}/{pdf_count}] {pdf_path}を登録します...')
                handle_uploaded_file(f)


def files(path, only_ext_list=None):
    for pathname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if only_ext_list is not None and ext not in only_ext_list:
                continue
            yield os.path.join(pathname, filename)


def extract_title(path):
    _dir, _file = os.path.split(path)
    _title, ext = os.path.splitext(_file)
    return _title
