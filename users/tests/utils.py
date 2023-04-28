from pytest import fixture
from users.models import MyUser

@fixture
def setup_db(scope = 'class'):
    MyUser.objects.create_user(
        username = 'devid',
        email = 'devid@devid.com',
        password = 'devid3939!'
    )
    MyUser.objects.create_user(
        username = 'teste',
        email = 'teste@teste.com',
        password = 'teste3939!'
    )
    MyUser.objects.create_superuser(
        username = 'admin',
        email = 'admin@admin.com',
        password = 'asuna333@@'
    )
