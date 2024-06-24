from django.contrib import admin
from .models import Category, News, ContactDetails
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register


class NewsArticleModelAdmin(ModelAdmin):
    model = News
    menu_label = 'News'
    menu_icon = 'doc-full-inverse'  # Change this to the appropriate icon
    list_display = ('news_title', 'published_date', 'category')
    search_fields = ('news_title', 'description')
    list_filter = ('category',)


modeladmin_register(NewsArticleModelAdmin)


class ContactDetailsAdmin(ModelAdmin):
    model = ContactDetails
    menu_label = 'News Requests'
    menu_icon = 'doc-full-inverse'  # change as needed
    list_display = ('username', 'phone_number', 'email')
    search_fields = ('username', 'email')


modeladmin_register(ContactDetailsAdmin)


class Category_Admin(ModelAdmin):
    model = Category
    menu_label = 'News Categories'
    menu_icon = 'tag'
    list_display = ('name', 'label')
    search_fields = ('name', 'label')


modeladmin_register(Category_Admin)
