import os
import unittest

from miskatonic.models import Article, Category


class MainTests(unittest.TestCase):
    def setUp(self):
        self.db_name = 'MISKATONIC_DB'
        os.environ[self.db_name] = 'test.db'

    def test_create_category(self):
        cat = Category.create(title='python')
        self.assertEqual(cat.title, 'python')
        cat.delete_instance(recursive=True)

    def test_create_article(self):
        cat = Category.create(title='python')
        article = Article.create(title='test', content='meh', category=cat)
        self.assertEqual(article.slug, 'test')
        cat.delete_instance(recursive=True)


if __name__ == '__main__':
    unittest.main()
