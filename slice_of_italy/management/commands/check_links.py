from django.core.management.base import BaseCommand
from django.urls import get_resolver
from django.test import Client

class Command(BaseCommand):
    help = 'Check for broken links in the project.'

    def handle(self, *args, **options):
        client = Client()
        urlconf = get_resolver().url_patterns

        def check_urls(urls, prefix=''):
            for url in urls:
                if hasattr(url, 'url_patterns'):
                    check_urls(url.url_patterns, prefix + url.pattern.regex.pattern)
                else:
                    try:
                        response = client.get(prefix + url.pattern.regex.pattern)
                        if response.status_code != 200:
                            self.stdout.write(self.style.ERROR(f'Broken link: {prefix + url.pattern.regex.pattern} (status code: {response.status_code})'))
                        else:
                            self.stdout.write(self.style.SUCCESS(f'Working link: {prefix + url.pattern.regex.pattern}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error accessing {prefix + url.pattern.regex.pattern}: {e}'))

        check_urls(urlconf)
