import glob
import logging
import re
from collections import namedtuple

from bulk_update.helper import bulk_update

from book.constants import BOOK_STATUS_UPLOADED
from book.models import Author, Category, Book, BookImage
import os.path
import os

from pdf2image import convert_from_path
from tqdm import tqdm

import time

from celery import task

import zipfile

# from utils.pdf import PDFConverter
from subprocess import Popen, PIPE


@task
def update_book_data(book_id, pdf_path, thumbnail_dir):
    """
    時間がかかりそうな取得系はこのメソッド内で取得
    ・ページ数
    ・サムネイル取得（本の1枚目）

    :param book_id: Book Model pk
    :param pdf_path: 保存済みpdf_path
    :param thumbnail_dir: サムネイル保存先ディレクトリ
    :return:
    """
    _book = Book.objects.filter(pk=book_id).first()
    # ページ数更新
    _book.page_count = page_count(pdf_path)
    # サムネイル設定
    thumbnail_path_new = f'{thumbnail_dir}/thumbnail.png'
    convert_from_path(pdf_path, last_page=1, output_folder=thumbnail_dir, fmt='png')
    thumbnail_path_old = sorted(glob.glob(f'{thumbnail_dir}/*.png'))[0]
    os.rename(thumbnail_path_old, thumbnail_path_new)
    _book.thumbnail_image = thumbnail_path_new

    _book.save()


@task
def save_pdf2images(book_id, pdf_path, save_dir):
    """
    pdfを画像.pngに変換し保存
    :param book_id: Book Model pk
    :param pdf_path: 保存済みpdf_path
    :param save_dir: Image 保存先ディレクトリ
    :return:
    """

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    _book = Book.objects.filter(pk=book_id).first()

    def convert_pdf2img_save(first_page=None, last_page=None):
        nonlocal _book
        # output_folderを指定しないとメモリエラーになる
        convert_from_path(pdf_path, output_folder=save_dir, first_page=first_page, last_page=last_page, fmt='png')
        # 名前の変更
        path_list = sorted(glob.glob(f'{save_dir}/*.png'))
        new_path_list = []
        new_index_list = []
        for path in path_list:
            new_filename = os.path.basename(path).split('-')[-1]
            img_index = int(new_filename.split('.')[0])
            new_path = f'{save_dir}/{new_filename}'
            os.rename(path, new_path)
            new_path_list.append(new_path)
            new_index_list.append(img_index)

        # Bookに紐づく画像の保存
        book_image_list = [BookImage(image=path, book=_book, page=i)
                           for (i, path) in zip(new_index_list, new_path_list)]
        BookImage.objects.bulk_create(book_image_list)

    # サムネイル用に早めに1枚目だけやっとく
    convert_pdf2img_save(last_page=1)
    convert_pdf2img_save(first_page=2)

    # Bookのステータス更新
    _book.status = BOOK_STATUS_UPLOADED
    _book.save()

    # TODO: 通知


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
        save_pdf_path = f'{save_dir}/{pdf_title}.pdf'
        logging.debug(f'save pdf {save_pdf_path}')
        with open(save_pdf_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        # zip保存
        save_zip_path = f'{save_dir}/{pdf_title}.zip'
        with zipfile.ZipFile(save_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            new_zip.write(save_pdf_path, arcname=f'{pdf_title}.pdf')

        # DB登録
        _book = Book.objects.create(title=pdf_title,
                                    page_count=0,
                                    pdf_file=save_pdf_path,
                                    zip_file=save_zip_path)

        # 非同期：jpeg変換、保存
        save_imgs_dir = f'{save_dir}/images'
        logging.debug(f'save images {save_imgs_dir}')
        save_pdf2images.delay(_book.pk, save_pdf_path, save_imgs_dir)

        # 非同期：情報更新：ページ数, サムネイル
        logging.debug(f'update book data')
        update_book_data.delay(_book.pk, save_pdf_path, save_dir)

        # ファイル情報取得
        # pdf_isnfo = extract_pdf_file_info(save_pdf_path)

        # _category = None
        # if category:
        #     _category, _ = Category.objects.get_or_create(content=category)

        if author_name:
            _author, _ = Author.objects.get_or_create(name=author_name)
            _book.author.set([_author])



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


def page_count(pdf_path, userpw=None):
    try:
        if userpw is not None:
            proc = Popen(["pdfinfo", pdf_path, '-upw', userpw], stdout=PIPE, stderr=PIPE)
        else:
            proc = Popen(["pdfinfo", pdf_path], stdout=PIPE, stderr=PIPE)

        out, err = proc.communicate()
    except:
        raise Exception('Unable to get page count. Is poppler installed and in PATH?')

    try:
        # This will throw if we are unable to get page count
        return int(re.search(r'Pages:\s+(\d+)', out.decode("utf8", "ignore")).group(1))
    except:
        raise Exception('Unable to get page count. %s' % err.decode("utf8", "ignore"))
