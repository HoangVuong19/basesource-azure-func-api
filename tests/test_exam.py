from tests.base import BaseTestCase


class TestExample(BaseTestCase):
    
    def test_ex(self):
        response = self.client.get("/api/healthcheck")

        assert response.status_code == 200
