from django.contrib import admin
from .models import Author, Genre, Language, Book, BookInstance
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Register your models here.
admin.site.register(Language)
#admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)

class BooksInstanceInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInstanceInline]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

class AvailabilityFilter(admin.SimpleListFilter):
    title = _('빌림 혹은 기부')
    parameter_name = 'Availability'

    def lookups(self, request, model_admin):
        return (
            ('isAvailableForRent', _('빌릴 수 있음')),
            ('isAvailableForDonation', _('기부 받을 수 있음'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'isAvailableForRent':
            return queryset.filter(reserved__range=["1900-01-01 00:00:00", timezone.now()])\
                .filter(due=None)\
                .filter(rent_availability=True)
        if self.value() == 'isAvailableForDonation':
            return queryset.filter(reserved__range=["1900-01-01 00:00:00", timezone.now()])\
                .filter(due=None)\
                .filter(donate_availability=True)

@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ('book', 'due', 'id')
    list_filter = (AvailabilityFilter,)

    fieldsets = (
        ('책 정보', {
            'fields': ('id', 'book', 'summary')
        }),
        ('책 유효성', {
            'fields': ('due', 'rent_availability', 'donate_availability')
        }),
        ('책 위치', {
            'fields': ('location_longitude', 'location_latitude')
        }),
    )