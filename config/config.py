from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str
    Un_token: str
    prefix: str

    @property
    def return_settings_values(self):
        settings_dict = {
                        "token": self.token,
                        "Un_token": self.Un_token,
                        "prefix": self.prefix
                         }
        return settings_dict

    if __name__ == '__main__':
        model_config = SettingsConfigDict(env_file="../.env")
    else:
        model_config = SettingsConfigDict(env_file=".env")


settings_class = Settings()
settings = settings_class.return_settings_values