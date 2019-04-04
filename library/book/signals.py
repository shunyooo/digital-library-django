from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from book.models import Book


@receiver(m2m_changed, sender=Book.tag.through)
def chaned_book_tag(sender, instance, **kwargs):
    tag_list = instance.tag.all()
    print('chaned_book_tag', tag_list)
    for tag in tag_list:
        tag.book_count = Book.objects.filter(tag=tag).count()
        tag.save()