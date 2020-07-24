from zygoat.components import Component
from zygoat.components.backend.reformat import reformat

from .deployment import deployment
from .email import email
from .simple_jwt import simple_jwt
from .tokens import token_util
from .chat import chat
from .django_willing_zg import django_willing_zg
from .get_env import get_env_util
from .secrets_manager import secrets_manager_util
from .secrets import secrets_util
from .google_analytics import google_analytics


class AllComponents(Component):
    pass


all_components = AllComponents(
    sub_components=[
        deployment,
        email,
        simple_jwt,
        token_util,
        reformat,
        chat,
        django_willing_zg,
        get_env_util,
        secrets_manager_util,
        secrets_util,
        google_analytics,
    ]
)
