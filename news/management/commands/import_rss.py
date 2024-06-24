import re
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import feedparser
from dateutil import parser as date_parser
from News.models import News, Page  # Adjust import according to your app structure
from News.utils import save_image_from_url  # Adjust import according to your utility function


class Command(BaseCommand):
    help = 'Import RSS feed entries into the NewsArticle model'

    def handle(self, *args, **kwargs):
        rss_urls = {
            "https://feeds.bbci.co.uk/news/rss.xml": "general",
            "https://rss.cnn.com/rss/edition.rss": "general",
            "https://www.yahoo.com/news/rss": "general",
            "https://www.thenews.com.pk/rss/1/1": "general",
            "https://www.thenews.com.pk/rss/1/8": "general",
            "https://www.thenews.com.pk/rss/2/14": "general",
            "https://feeds.bbci.co.uk/news/world/rss.xml": "world",
            "https://feeds.bbci.co.uk/news/business/rss.xml": "business",
            "https://feeds.bbci.co.uk/news/health/rss.xml": "health",
            "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml": "entertainment",
            "https://feeds.bbci.co.uk/news/world/asia/rss.xml": "asia",
            "https://feeds.bbci.co.uk/news/technology/rss.xml": "technology",
            "https://feeds.bbci.co.uk/news/world/europe/rss.xml": "world",
            "https://feeds.bbci.co.uk/news/world/africa/rss.xml": "africa",
            "http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/cricket/rss.xml": "sports",
            "https://feeds.bbci.co.uk/news/politics/rss.xml": "politics",
            "https://feeds.bbci.co.uk/news/wales/rss.xml": "wales",
            "https://feeds.bbci.co.uk/news/scotland/rss.xml": "scotland",
            "https://feeds.bbci.co.uk/news/northern_ireland/rss.xml": "northernIreland",
            "https://feeds.bbci.co.uk/news/england/rss.xml": "england",
            "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml": "usCanada",
            "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml": "middleEast",
            "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml": "latinAmerica",
            # Your RSS URLs and categories here...
        }

        home_page = Page.objects.get(slug='home')  # Ensure you have a home page

        for rss_url, category in rss_urls.items():
            feed = feedparser.parse(rss_url)
            entries = feed.entries

            for entry in entries:
                title = entry.get('title')
                link = entry.get('link')[:200]  # Truncate link if it exceeds 200 characters
                summary = entry.get('summary', 'No description available.')

                published_date_str = entry.get('published')
                published_date = date_parser.parse(published_date_str) if published_date_str else None

                # Extract image URL based on feed structure
                if 'media_thumbnail' in entry and entry['media_thumbnail']:
                    image_url = entry['media_thumbnail'][0]['url']
                elif 'media:content' in entry and entry['media:content']:
                    image_url = entry['media:content']['url']
                elif 'media:thumbnail' in entry and entry['media:thumbnail']:
                    image_url = entry['media:thumbnail']['url']
                else:
                    cdata_content = entry.get('description')
                    match = re.search(r'<img src="([^"]+)"', cdata_content) if cdata_content else None
                    image_url = match.group(1) if match else None

                # Generate a unique slug
                slug = self.get_unique_slug(title)

                # Check if the news article already exists
                news_article = NewsArticle.objects.child_of(home_page).filter(slug=slug).first()

                if news_article:
                    # Update existing article
                    news_article.link = link
                    news_article.description = summary
                    news_article.published_date = published_date
                    news_article.category = category

                    if image_url:
                        image_content = save_image_from_url(image_url, title, f"{slug}.jpg")
                        if image_content:
                            news_article.image_url.save(
                                f"{slug}.jpg",
                                image_content,
                                save=False
                            )

                    news_article.save()
                else:
                    # Create new article
                    news_article = NewsArticle(
                        title=title,
                        slug=slug,
                        news_title=title,
                        link=link,
                        description=summary,
                        published_date=published_date,
                        category=category,
                    )

                    if image_url:
                        image_content = save_image_from_url(image_url, title, f"{slug}.jpg")
                        if image_content:
                            news_article.image_url.save(
                                f"{slug}.jpg",
                                image_content,
                                save=False
                            )

                    home_page.add_child(instance=news_article)
                    news_article.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported RSS feed entries'))

    def get_unique_slug(self, title):
        # Generate a unique slug by appending a number to the title
        slug = slugify(title)
        base_slug = slug
        counter = 1

        while NewsArticle.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug
