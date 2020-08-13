import logging

from zygoat.components import Component, SettingsComponent

log = logging.getLogger()


get_secret_function_string = """def get_secret(secret_arn):
    \"\"\"Create a Secrets Manager client\"\"\"
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_arn
    )
    return get_secret_value_response
"""


class SecretsManagerSettings(SettingsComponent):
    def create(self):
        red = self.parse()

        first_import_index = red.index(red.find("importnode"))

        log.info("Inserting boto3 import into django settings")
        red.insert(first_import_index + 1, "import boto3")

        log.info("Inserting get_secret function")
        index = red.index(red.find("name", "PRODUCTION").parent)
        red.insert(index + 1, "\n")
        red.insert(index + 2, "\n")
        red.insert(index + 3, get_secret_function_string)

        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        return red.find("def", "get_secret") is not None


class SecretsManager(Component):
    pass


secrets_manager_util = SecretsManager(sub_components=[SecretsManagerSettings()])
