import pytest
from users.models import MyUser
from posts.models import Post, Comment
from users.utils import setup_users_on_db
from posts.utils import setup_posts_on_db, setup_comments_on_db

@pytest.mark.django_db
class TestCommentModel:
    def test_create(self, faker, setup_posts_on_db):
        user = MyUser.objects.get(id = 1)
        expected_comment = Comment.objects.create(
            content = faker.text(),
            author = user,
            post = Post.objects.get(id = 1)
        )
        comment = Comment.objects.get(id = 1)
        assert expected_comment == comment

    def test_update(self, faker, setup_comments_on_db):
        comments = Comment.objects.all()
        expected_comment = []
        for comment in comments:
            comment.content = faker.text()
            comment.save(update_fields = ['content'])
            expected_comment.append(comment)
        comments = Comment.objects.all()
        for c in range(0, len(expected_comment)):
            assert expected_comment[c] == comments[c]

    def test_delete(self, setup_comments_on_db):
        comments = Comment.objects.all()
        for comment in comments:
            comment.delete()
        assert len(Comment.objects.all()) == 0
    
    def test_delete_posts(self, setup_comments_on_db):
        posts = Post.objects.all()
        for post in posts:
            post.delete()
        assert len(Comment.objects.all()) == 0
