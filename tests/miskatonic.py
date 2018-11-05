import os
import unittest

from miskatonic.apps.blog.models import Article


class MainTests(unittest.TestCase):
    def setUp(self):
        self.db_name = 'MISKATONIC_DB'
        os.environ[self.db_name] = 'test.db'

    def test_create_article(self):
        article = Article.create(title='test', content='meh')
        self.assertEqual(article.slug, 'test')
        article.delete_instance(recursive=True)


if __name__ == '__main__':
    unittest.main()
