from enum import Enum


class EnvironmentEnum(Enum):
    production = "production"
    stage = "stage"
    development = "development"
    local = "local"

    @classmethod
    def allowable_environments(cls):
        return cls.production.value, cls.stage.value, cls.development.value
