from django.test import TestCase
from django.utils import timezone

from .models import List, Restaurant


# Create your tests here.

class ListModelTests(TestCase):
    def test_list_cration(self):
        r_list=List.objects.create(
                title="Hola",
                description="Fatty fat tuna"
        )
        now = timezone.now()
        self.assertLess(r_list.created_at, now)
