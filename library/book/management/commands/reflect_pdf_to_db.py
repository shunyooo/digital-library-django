from django.core.management.base import BaseCommand

from book.models import Book
from ...tasks import handle_uploaded_file
import os


class Command(BaseCommand):
    help = 'Reflect Existing PDF to DB'

    def add_arguments(self, parser):
        parser.add_argument('pdf_dir', nargs='+', type=str)
        parser.add_argument('--f', action='store_true')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        # pdf fileの走査
        taget_pdf_path_list = []
        for pdf in options['pdf_dir']:
            taget_pdf_path_list += list(files(pdf, only_ext_list=['.pdf']))
        target_pdf_name_list = [extract_title(path) for path in taget_pdf_path_list]

        # DBにすでにあるpdfを全取得
        db_pdf_path_list = [book.pdf_file.name for book in Book.objects.all()]
        db_pdf_name_list = [extract_title(path) for path in db_pdf_path_list]

        # 未登録の本を抽出
        unregistered_pdf_path_list = [path for name, path in zip(target_pdf_name_list, taget_pdf_path_list)
                                      if name not in db_pdf_name_list]

        njoin = lambda _list: '\n'.join(_list)
        print(f"""
【登録済み】\n{njoin([path for path in target_pdf_name_list if path not in unregistered_pdf_path_list])}

【未登録】\n{njoin(unregistered_pdf_path_list)}
        """)

        print(f'{len(taget_pdf_path_list)}件のPDFが見つかりました。\nその内{len(unregistered_pdf_path_list)}件が未登録です。')

        is_all_registered = len(unregistered_pdf_path_list) == 0
        if is_all_registered:
            print('\n全件登録済みです！終了します...')
            return

        is_force = 'f' in options and options['f']
        if not is_force:
            print('DBに登録しますか？')
            while (True):
                yn_input = input('y/n: ').lower()
                if 'y' == yn_input:
                    break
                elif 'n' == yn_input:
                    print('cancel')
                    return
                else:
                    print('入力が不正です')

        pdf_count = len(unregistered_pdf_path_list)
        for i, pdf_path in enumerate(unregistered_pdf_path_list):
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
