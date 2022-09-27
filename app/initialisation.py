from typing import List, Dict, Any

from astropy.table import Row
from astroquery.mast import Observations
from numpy.ma.core import MaskedConstant

from app.models.database import db
from app.models import observations
from app import schemas
from pydantic import parse_obj_as

mission = "JWST"
calib_levels = [2, 3]  # equivalent to 2 = calibrated, 3 = science product
data_product_type = "IMAGE"  # can be IMAGE, SPECTRUM, SED, TIMESERIES, VISIBILITY, EVENTLIST, CUBE, CATALOG, ENGINEERING, NULL


def convert_masked_constant(value: Any) -> Any:
    """
    Basic conversion to deal with MaskedConstants - cannot convert otherwise.
    :param value:
    :return:
    """
    if isinstance(value, MaskedConstant):
        return None
    return value


def row_adaptor(row: Row) -> Dict:
    return {col: convert_masked_constant(row[col]) for col in row.colnames}


def get_observations(levels, instrument_name, filters) -> List[Dict]:
    """
    Returns a list of rows of observations from NIRCam given the specified levels
    :param levels:
    :return:
    """
    observations = list()
    for level in levels:
        observations = [
            *observations,
            *list(
                Observations.query_criteria(
                    obs_collection=mission,
                    calib_level=level,
                    dataproduct_type=data_product_type,
                    instrument_name=instrument_name,
                    filters=filters,
                )
            ),
        ]

    return list(map(row_adaptor, observations))


# from the rows we can zip keys and values to get stuff to put into the db.


def get_images(obs_list):
    # get the product list
    prod_list = Observations.get_product_list(obs_list)
    return prod_list


if __name__ == "__main__":
    obs: List[Dict] = get_observations(
        levels=calib_levels,
        instrument_name="nircam",
        filters=[
            "F070W",
            "F090W",
            "F115W",
            "F150W",
            "F200W",
            "F277W",
            "F356W",
            "F444W",
        ],
    )
    print(obs)
    db.connect()
    with db.atomic():
        for idx in range(0, len(obs), 100):
            validated: List[schemas.MastObservationBase] = parse_obj_as(
                list[schemas.MastObservationBase], obs[idx : idx + 100]
            )
            values = [
                list(validated_obj.dict().values()) for validated_obj in validated
            ]
            observations.MastObservation.insert_many(values).execute()
    db.close()

    for ob in obs:
        prods = get_images(obs_list=ob)
        print(prods)
