from django.core.management.base import BaseCommand
from django.db.models import Q

from book.models import Book, Tag


class Command(BaseCommand):
    help = 'Allocate tag to multi book by contain title'

    def add_arguments(self, parser):
        parser.add_argument('--tag', nargs=1, type=str, help='Tag name for set', metavar=('DeepLearning',),
                            required=True)
        parser.add_argument('--contains', nargs='+', type=str, help='Contains name list', metavar=('Deep', '深層'),
                            required=True)

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        tag = options['tag'][0]
        contains_pat_list = options['contains']
        allocate_tag(tag, contains_pat_list)


def allocate_tag(tag: str, pat: list) -> None:
    """
    tagをpatternにあう本に割り当てる
    """
    tag_obj, is_create = Tag.objects.get_or_create(content=tag)

    # 抽出
    book_match_q = Book.objects.filter(filter_icontains(pat))
    registered_book_q = book_match_q.filter(tag__pk=tag_obj.pk).distinct()
    unregistered_book_q = book_match_q.exclude(tag__pk=tag_obj.pk).distinct()

    print('-' * 50)
    print(f'# タグ:「{tag}」, contain パターン:{pat}\n')
    titlejoin = lambda q: '\n'.join([book.title for book in q])
    print('【登録済み】:\n', titlejoin(registered_book_q))
    print('\n【未登録】:\n', titlejoin(unregistered_book_q))

    if len(unregistered_book_q) == 0:
        print('全件割り当て済みです。')
        return
    else:
        print(f'{len(unregistered_book_q)}件割り当て可能です。「{tag}」を割りあてますか？')

    if 'y' not in input('y/n: ').lower():
        print('cancel.')
        return

    # 割り当て
    for book in unregistered_book_q:
        book.tag.add(tag_obj)


def filter_icontains(pat_list):
    pat_q_list = [Q(title__icontains=p) for p in pat_list]
    query = pat_q_list.pop()
    for _q in pat_q_list:
        query |= _q
    return query
