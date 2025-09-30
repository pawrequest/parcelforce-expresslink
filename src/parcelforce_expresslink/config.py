import functools
import os
from importlib.resources import files
from pathlib import Path

from loguru import logger
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def load_env():
    ship_env = Path(os.getenv('PARCELFORCE_ENV'))
    if not ship_env.exists():
        raise ValueError('PARCELFORCE_ENV not set correctly')
    logger.debug(f'Loading PARCELFORCE environment from {ship_env}')
    return ship_env


def get_wsdl():
    res = Path(files('parcelforce_expresslink').joinpath('expresslink_api.wsdl'))
    if not res.exists():
        raise FileNotFoundError('WSDL file not found')
    logger.info(f'Using WSDL file at {res}')
    return res


class PFSettings(BaseSettings):
    """Load Parcelforce ExpressLink configuration from environment variables / .env file.
    location of environment file is set by the environment variable PARCELFORCE_ENV.
    """

    pf_ac_num_1: str
    pf_ac_num_2: str | None
    pf_contract_num_1: str
    pf_contract_num_2: str | None
    department_id: int = 1

    pf_expr_usr: SecretStr
    pf_expr_pwd: SecretStr
    pf_endpoint: str
    pf_wsdl: str = Field(default_factory=get_wsdl)
    pf_binding: str = r'{http://www.parcelforce.net/ws/ship/v14}ShipServiceSoapBinding'
    tracking_url_stem: str = r'https://www.royalmail.com/track-your-item#/tracking-results/'

    model_config = SettingsConfigDict(env_ignore_empty=True, env_file=load_env())

    def get_auth_secrets(self) -> tuple[str, str]:
        return self.pf_expr_usr.get_secret_value(), self.pf_expr_pwd.get_secret_value()


@functools.lru_cache
def pf_settings() -> PFSettings:
    return PFSettings()

