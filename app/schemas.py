from typing import Any, List

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


# Example only TODO add the real model schemas.
class User(BaseModel):
    id: int
    is_active: bool
    items: List = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class DataProductBase(BaseModel):
    obsID: str
    obs_id: str
    description: str
    type: str
    dataURI: str


class DataProduct(DataProductBase):
    id: int
    observation_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class MastObservationBase(BaseModel):
    dataproduct_type: str
    calib_level: int
    obs_collection: str
    obs_id: str
    target_name: str
    s_ra: float
    s_dec: float
    t_min: float
    t_max: float
    t_exptime: float
    wavelength_region: str
    filters: str
    em_min: float
    em_max: float
    target_classification: str | None
    obs_title: str
    t_obs_release: float
    instrument_name: str
    proposal_pi: str
    proposal_id: str
    proposal_type: str
    project: str
    sequence_number: int | None
    provenance_name: str
    s_region: str
    jpegURL: str | None
    dataURL: str
    dataRights: str
    mtFlag: bool
    srcDen: float | None
    intentType: str
    obsid: int
    objID: str


class MastObservation(MastObservationBase):
    id: int
    data_products: List[DataProduct] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
