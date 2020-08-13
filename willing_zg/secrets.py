import logging

from zygoat.components import Component, SettingsComponent

log = logging.getLogger()

# Get secrets from serets manager via get_secret() function

database_secret = """if "DATABASE_SECRET" in os.environ:
    db_secret = json.loads(get_secret(os.environ["DATABASE_SECRET"])["SecretString"])

    db_username = db_secret["username"]
    db_password = db_secret["password"]
    db_host = db_secret["host"]
    db_port = str(db_secret["port"])
    db_clusterid = db_secret["dbClusterIdentifier"]

    db_url = f"postgres://{db_username}:{db_password}@{db_host}:{db_port}/{db_clusterid}"
    os.environ["DATABASE_URL"] = db_url
"""

email_host_password = """if "DJANGO_EMAIL_HOST_PASSWORD" in os.environ:
    django_password = json.loads(get_secret(os.environ["DJANGO_EMAIL_HOST_PASSWORD"])["SecretString"])
    EMAIL_HOST_PASSWORD = django_password["DJANGO_EMAIL_HOST_PASSWORD"]
"""


class SecretsSettings(SettingsComponent):
    def create(self):
        red = self.parse()

        first_import_index = red.index(red.find("importnode"))

        log.info("Inserting json import into django settings")
        red.insert(first_import_index + 1, "import json")

        log.info("Inserting retrieving database secret")
        index = red.index(red.find("comment", value="# Database"))
        red.insert(index + 2, "\n")
        red.insert(index + 3, database_secret)

        log.info("Inserting setting django email host password")
        index = red.index(red.find("name", "EMAIL_HOST_PASSWORD").parent)
        red.insert(index + 1, email_host_password)

        self.dump(red)

    @property
    def installed(self):
        red = self.parse()
        dbSecretInstalled = red.find("name", value="db_secret")
        djangoEmailInstalled = red.find("name", "EMAIL_HOST_PASSWORD")
        return dbSecretInstalled is not None and djangoEmailInstalled is not None


class Secrets(Component):
    pass


secrets_util = Secrets(sub_components=[SecretsSettings()])
