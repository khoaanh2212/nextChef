from start_server_util import start_server
from backend.settings import test


start_server('test', 'backend.settings.test', *test.LOCAL_APPS)