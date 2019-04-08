import logging
import os

from django.db.models.signals import m2m_changed, post_delete, pre_delete
from django.dispatch import receiver

from book.models import Book
import shutil


@receiver(m2m_changed, sender=Book.tag.through)
def chaned_book_tag(sender, instance, action, **kwargs):
    '''
    book-tag が変更されたら tagのbookcountを変更。
    book 削除時に呼ばれないバグがある。
    https://stackoverflow.com/questions/46782056/django-no-m2m-changed-signal-when-one-side-of-a-many-to-many-is-deleted
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    '''
    tag_list = instance.tag.all()
    logging.debug(f'action:{action} chaned_book_tag:{tag_list}')
    count_func = lambda tag: Book.objects.filter(tag=tag).count()
    update_tag_book_count(instance, count_func)


@receiver(pre_delete, sender=Book)
def deleted_book(sender, instance, **kwargs):
    """
    本の削除時
    - tagのbook_countの更新
    - 本ファイルの削除
    """
    print('deleted:', instance.title, instance.tag.all())
    # 本がdeleteされる時でもtagのカウントを更新する。
    # preではまだ消されていないので、一旦デクリメントで対応。
    # （改善案：Bookの論理削除からpost_deleteでの再集計。）
    count_func = lambda tag: tag.book_count - 1
    update_tag_book_count(instance, count_func)

    # NOTE: Bookのフォルダがpdf_fileの一つ上にある前提。
    if instance.pdf_file:
        book_dir = os.path.dirname(instance.pdf_file.path)
        if os.path.isdir(book_dir):
            logging.debug(f'shutil delete {book_dir}')
            shutil.rmtree(book_dir)
        else:
            logging.warning(f'book media dir not found: {book_dir}')


def update_tag_book_count(book, count_func):
    """
    BookのTagのbook_countを更新。集計方法はcount_funcに。
    :param book:
    :param count_func:
    :return:
    """
    tag_list = book.tag.all()
    for tag in tag_list:
        new_book_count = count_func(tag)
        logging.debug(f'{tag} count: {tag.book_count} → {new_book_count}')
        if new_book_count == 0:
            logging.debug(f'delete {tag}')
            tag.delete()
        else:
            tag.book_count = new_book_count
            tag.save()
