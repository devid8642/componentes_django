import pytest
from posts.models import Post
from users.models import MyUser
from users.utils import setup_users_on_db
from posts.utils import setup_posts_on_db

@pytest.mark.django_db
class TestPostModel:
    def test_create(self, faker, setup_users_on_db):
        user = MyUser.objects.get(id = 1)
        expected_post = Post.objects.create(
            title = faker.name(),
            content = faker.text(),
            author = user
        )
        post = Post.objects.get(id = 1)
        assert post == expected_post
    def test_update(self, faker, setup_posts_on_db):
        post1 = Post.objects.get(id = 1)
        post2 = Post.objects.get(id = 2)
        post3 = Post.objects.get(id = 3)
        post1.title = faker.name()
        post2.content = faker.text()
        post3.title = faker.name()
        post3.content = faker.text()
        post1.save(update_fields = ['title'])
        post2.save(update_fields = ['content'])
        post3.save(update_fields = ['title', 'content'])
        assert post1 == Post.objects.get(id = 1)
        assert post2 == Post.objects.get(id = 2)
        assert post3 == Post.objects.get(id = 3)

    def test_delete(self, setup_users_on_db):
        posts = Post.objects.all()
        for post in posts:
            post.delete()
        assert len(Post.objects.all()) == 0
