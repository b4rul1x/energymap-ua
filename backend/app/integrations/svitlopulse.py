import httpx
from datetime import datetime
from pydantic import BaseModel, ValidationError, computed_field

BASE_URL = "https://svitlopulse.andrewboyko.name/api/v1"


class SourceError(Exception):
    """Джерело даних недоступне або повернуло некоректну відповідь."""


class OblastStatus(BaseModel):
    slug: str
    iso: str
    name_uk: str
    state: str
    off_share: float | None = None
    groups: int = 0
    groups_off: int = 0
    emergency: bool = False
    stale: bool = False
    updated_at: datetime | None = None
    operators: list[str] | None = None
    @computed_field
    @property
    def has_data(self) -> bool:
        return self.state != "unknown" and not self.stale


class OblastsResponse(BaseModel):
    oblasts: list[OblastStatus]


async def fetch_oblasts() -> list[OblastStatus]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/oblasts")
            response.raise_for_status()
        return OblastsResponse.model_validate(response.json()).oblasts
    except (httpx.HTTPError, ValidationError, ValueError) as exc:
        raise SourceError(f"SvitloPulse: {exc}") from exc