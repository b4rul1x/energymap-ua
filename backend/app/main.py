from fastapi import FastAPI, HTTPException
from backend.app.integrations.svitlopulse import OblastStatus, SourceError, fetch_oblasts
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI(title="EnergyMap UA")


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

class Region(BaseModel):
    id: int
    name: str


REGIONS = [
    Region(id=1, name="Вінницька область"),
    Region(id=2, name="Волинська область"),
    Region(id=3, name="Дніпропетровська область"),
    Region(id=4, name="Донецька область"),
    Region(id=5, name="Житомирська область"),
    Region(id=6, name="Закарпатська область"),
    Region(id=7, name="Запорізька область"),
    Region(id=8, name="Івано-Франківська область"),
    Region(id=9, name="Київська область"),
    Region(id=10, name="Кіровоградська область"),
    Region(id=11, name="Луганська область"),
    Region(id=12, name="Львівська область"),
    Region(id=13, name="Миколаївська область"),
    Region(id=14, name="Одеська область"),
    Region(id=15, name="Полтавська область"),
    Region(id=16, name="Рівненська область"),
    Region(id=17, name="Сумська область"),
    Region(id=18, name="Тернопільська область"),
    Region(id=19, name="Харківська область"),
    Region(id=20, name="Херсонська область"),
    Region(id=21, name="Хмельницька область"),
    Region(id=22, name="Черкаська область"),
    Region(id=23, name="Чернівецька область"),
    Region(id=24, name="Чернігівська область"),
    Region(id=25, name="м. Київ"),
    Region(id=26, name="Автономна Республіка Крим"),
]


@app.get("/api/v1/regions", response_model=list[Region])
def get_regions():
    return REGIONS

class MapStatusResponse(BaseModel):
    source: str
    fetched_at: datetime
    regions: list[OblastStatus]


@app.get("/api/v1/map/status", response_model=MapStatusResponse)
async def map_status():
    try:
        regions = await fetch_oblasts()
    except SourceError:
        raise HTTPException(status_code=503, detail="Джерело даних тимчасово недоступне")
    return MapStatusResponse(
        source="SvitloPulse",
        fetched_at=datetime.now(timezone.utc),
        regions=regions,
    )