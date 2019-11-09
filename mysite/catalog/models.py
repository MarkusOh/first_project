from django.db import models
from django.urls import reverse
import datetime
from django.utils import timezone

import uuid  # 고유한 책 UID를 위해 필요합니다

"""책의 장르를 데이터베이스에서 관리하기 쉽도록 모델로 만듭니다"""


class Author(models.Model):
    """작가를 표현하는 모델입니다"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """특정한 작가를 소개하는 URL을 반환합니다"""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Genre(models.Model):
    """책의 장르를 표현하는 모델입니다"""
    name = models.CharField(max_length=200, help_text='책 장르를 입력하세요!')

    def __str__(self):
        return self.name


class Language(models.Model):
    """언어를 표현하는 모델입니다"""
    name = models.CharField(
        max_length=200,
        help_text="책 언어를 입력하세요"
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    """책을 표현하는 모델입니다"""
    title = models.CharField(max_length=200)

    # 한 작가는 여러 책을 쓸 수 있되, 한 책은 여러 작가를 가질 수 없습니다.
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text
        ='13 글자로 이루어진 <a href="https://www.isbn-international.org/content/what-isbn">ISBN 넘버를 입력하시오!</a>'
    )

    # 책과 장르는 다대다 관계를 갖습니다. 위에 정의된 Genre Class를 사용해 명시하겠습니다
    genre = models.ManyToManyField(Genre, help_text='장르를 선택하시오!')

    # 책이 어떤 언어로 되어있는지 표현합니다
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # 이 모델의 레코드를 불러올 URL을 리턴합니다
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """관리자 웹페이지에서 쓰일 장르 표기 메소드입니다"""
        return ', '.join(genre.name for genre in self.genre.all())

class BookInstance(models.Model):
    """이 모델은 Book모델의 고유한 한권 한권을 표기합니다"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='한 권의 책에게만 부여되는 고유한 ID입니다')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    # 글쓴이가 책을 묘사할 수 있습니다
    summary = models.TextField(max_length=1000, help_text='간단한 책 설명 부탁드립니다!')

    # 가져다 줘야하는 시간 및 날짜입니다
    due = models.DateTimeField(null=True, blank=True)

    # 빌릴 수 있느냐?
    rent_availability = models.BooleanField()

    # 기부 받을 수 있느냐?
    donate_availability = models.BooleanField()

    # 현제 예약이 되어있느냐? 과거로 설정되어 있는 경우 예약이 없는 상태이다
    reserved = models.DateTimeField(auto_now=True)

    # 빌리거나 기부 받을 장소는 어디이느냐?
    location_longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    location_latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    class Meta:
        ordering = ['-due']

    def __str__(self):
        # 모델 객체를 표현하는 string
        return f'{self.id} ({self.book.title})'

    def isRentAvailable(self):
        return (self.reserved <= timezone.now() and self.due == None and self.rent_availability == True)

    def isDonationAvailable(self):
        return (self.reserved <= timezone.now() and self.due == None and self.donate_availability == True)
