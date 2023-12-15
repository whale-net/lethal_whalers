import os
from pydantic import BaseModel


class Manifest(BaseModel):
    name: str
    description: str
    version_number: str
    website_url: str
    dependencies: list[str]

    def update_version(self, major: int, minor: int, patch: int):
        # use environment variable to get version
        self.version_number = f'{major}.{minor}.{patch}'