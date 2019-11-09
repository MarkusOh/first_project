from django.shortcuts import render
from django.utils import timezone
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic


def index(request):
    """홈페이지 View function입니다!"""

    # 메인 객체가 몇개 있나 세봅니다!
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # 빌리거나 기부 받을 수 있는 책들의 권수
    num_instances_available = BookInstance.objects.filter(reserved__range=["1900-01-01 00:00:00", timezone.now()]) \
        .filter(due=None).count()

    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book
