import pytest
from users.models import MyUser
from posts.models import Post
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
