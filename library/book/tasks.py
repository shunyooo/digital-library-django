import glob
import logging
from collections import namedtuple

from book.models import Author, Category, Book
import os.path
import os

from pdf2image import convert_from_path
from tqdm import tqdm

import time

from celery import task


# from utils.pdf import PDFConverter


@task
def save_pdf2images(pdf_path, save_dir):
    """
    pdfを画像.pngに変換し保存
    :param pdf_path: 保存済みpdf_path
    :param save_dir: 保存先ディレクトリ
    :return:
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # output_folderを指定しないとメモリエラーになる
    convert_from_path(pdf_path, output_folder=save_dir, fmt='png')
    # 名前の変更
    path_list = glob.glob(f'{save_dir}/*.png')
    for path in path_list:
        new_filename = os.path.basename(path).split('-')[-1]
        new_path = f'{save_dir}/{new_filename}'
        os.rename(path, new_path)


def handle_uploaded_file(f, author_name=None, category=None):
    """
    file（PDF）をmediaに保存。
    modelにBookを追加し、jpegに分割して保存。
    """
    try:
        # 該当ディレクトリ作成
        pdf_title, _ = os.path.splitext(f.name)
        save_dir = f'./media/{pdf_title}'
        os.makedirs(save_dir)

        # PDF保存
        save_pdf_path = f'{save_dir}/content.pdf'
        logging.debug(f'save pdf {save_pdf_path}')
        with open(save_pdf_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        # 非同期：jpeg変換、保存
        save_imgs_dir = f'{save_dir}/images'
        logging.debug(f'save images {save_imgs_dir}')
        save_pdf2images.delay(save_pdf_path, save_imgs_dir)

        # ファイル情報取得
        # pdf_isnfo = extract_pdf_file_info(save_pdf_path)

        # DB登録
        _book = Book.objects.create(title=pdf_title,
                                    page_count=0, )

        # _category = None
        # if category:
        #     _category, _ = Category.objects.get_or_create(content=category)

        if author_name:
            _author, _ = Author.objects.get_or_create(name=author_name)
            _book.author.set([_author])

        # TODO: APIより書籍情報を集める

        # TODO: 通知




    except Exception as e:
        import traceback;
        traceback.print_exc()
        raise Exception(e.args)
        # print("例外args:", e.args)


PdfInfo = namedtuple('PdfInfo', ('title', 'page_count'))


def extract_pdf_file_info(path):
    title = extract_pdf_title(path)
    return PdfInfo(title=title, page_count=0)


def extract_pdf_title(path):
    filename = os.path.basename(path)
    title, _ = os.path.splitext(filename)
    return title
