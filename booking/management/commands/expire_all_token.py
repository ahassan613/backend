from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.core.management.base import BaseCommand



# python manage.py update_product 1 123

class Command(BaseCommand):

    help = 'Remove User token'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for removing token')


    def handle(self, *args, **kwargs):
        username = kwargs['username']

        try:
            deleted_obj = OutstandingToken.objects.filter(user__username=username).delete()

            self.stdout.write('Tokens deleted for "%s"' % username)
        except:
            self.stdout.write('Unable to delete to token')