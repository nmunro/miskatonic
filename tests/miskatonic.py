from miskatonic import db
import os
import unittest


class MainTests(unittest.TestCase):
    def setUp(self):
        self.db_name = 'MISKATONIC_DB'
        os.environ[self.db_name] = 'test.db'
        db.create_tables()

    def test_create_category(self):
        cat = db.Category.create(title='python')
        self.assertEqual(cat.title, 'python')
        cat.delete_instance(recursive=True)

    def test_create_article(self):
        cat = db.Category.create(title='python')
        article = db.Article.create(title='test', content='meh', category=cat)
        self.assertEqual(article.slug, 'test')
        cat.delete_instance(recursive=True)


if __name__ == '__main__':
    unittest.main()
