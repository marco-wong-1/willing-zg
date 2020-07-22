from zygoat.components import Component
from zygoat.components.backend.reformat import reformat

from .deployment import deployment
from .email import email
from .simple_jwt import simple_jwt
from .tokens import token_util


class AllComponents(Component):
    pass


all_components = AllComponents(
    sub_components=[deployment, email, simple_jwt, token_util, reformat]
)
