from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class News(Page):
    # templates = "home/winszone_layouts/partials/header.html"
    published_date = models.DateField()
    news_title = models.CharField(max_length=255)
    description = RichTextField()
    link = models.URLField()
    image_url = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('published_date'),
        FieldPanel('news_title'),
        FieldPanel('description'),
        FieldPanel('link'),
        FieldPanel('image_url'),
        FieldPanel('category'),
    ]


class ContactDetails(Page):
    # templates = 'abc/abc.html'
    # intro = RichTextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('email'),
        FieldPanel('username'),
        FieldPanel('phone_number'),
    ]
