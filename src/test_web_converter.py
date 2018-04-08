from tornado.testing import AsyncHTTPTestCase





class ServletTestCase(AsyncHTTPTestCase):

    def test_get_conversion_one_usd_to_brl(self):
        response = self.fetch("/convert?from=USD&to=BRL&amount=1")
        assert "1" == response.text
