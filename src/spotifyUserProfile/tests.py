
from django.test import TestCase
from .models import TrackQuery

class TrackQueryTests(TestCase):
    def test_query_formatting(self):
        query = TrackQuery(query="Fight Club Blues, Brad Pitt")
        formatted = query.query.replace(' ', '+')
        self.assertEqual(formatted, "Fight+Club+Blues,+Brad+Pitt")
