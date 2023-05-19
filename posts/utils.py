import pytest
from users.models import MyUser
from posts.models import Post, Comment
from users.utils import setup_users_on_db

@pytest.fixture
def setup_posts_on_db(faker, setup_users_on_db):
    users = MyUser.objects.all()
    Post.objects.create(
        title = faker.name(),
        content = faker.text(),
        author = users[0]
    )
    Post.objects.create(
        title = faker.name(),
        content = faker.text(),
        author = users[1]
    )
    Post.objects.create(
        title = faker.name(),
        content = faker.text(),
        author = users[2]
    )

@pytest.fixture
def setup_comments_on_db(faker, setup_posts_on_db):
    users = MyUser.objects.all()
    posts = Post.objects.all()
    Comment.objects.create(
        content = faker.text(),
        author = users[0],
        post = posts[0]
    )
    Comment.objects.create(
        content = faker.text(),
        author = users[1],
        post = posts[1]
    )
    Comment.objects.create(
        content = faker.text(),
        author = users[2],
        post = posts[2]
    )
