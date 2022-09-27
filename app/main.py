from fastapi import FastAPI
from pydantic import BaseModel
from .models.database import db  # , db_state_default
from models.observations import MastObservation, DataProduct

db.create_tables([MastObservation, DataProduct])

app = FastAPI()


class Image(BaseModel):
    name: str
    description: str | None = None
    url: str


class ProcessedImage(BaseModel):
    image: Image
    target: str | None
    right_ascension: float | None
    declination: float | None


class ImageRequest(BaseModel):
    target: str
    right_ascension: float
    declination: float


class JWSTObservationData(BaseModel):
    dataproduct_type: str
    calib_level: int
    obs_id: str
    target_name: str
    s_ra: float
    s_dec: float
    t_min: float
    t_max: float
    t_exptime: float
    filters: str
    em_min: float
    em_max: float
    target_classification: str | None
    obs_title: str
    t_obs_release: float
    instrument_name: str
    proposal_pi: str
    proposal_id: str
    sequence_number: int
    s_region: str
    jpegURL: str
    dataURL: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


def find_observations(target_name: str):
    obs_list = list()
    # for observation in observations: TODO replace with db query.
    #     if observation["target_name"] == target_name:
    #         obs_list.append(observation)
    return obs_list


@app.get("/observations/{target_name}")
async def get_observations(target_name: str):
    observs = find_observations(target_name)
    return observs
