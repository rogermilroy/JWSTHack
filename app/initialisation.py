from typing import List, Dict, Any

from astropy.table import Row
from astroquery.mast import Observations
from numpy.ma.core import MaskedConstant

from app.mast_api.mast_api import (
    get_mast_request,
    MASTService,
    get_filter_params,
    mast_api_request,
)
from app.models import observations

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


def get_observations() -> List[Dict]:
    """
    Returns a list of rows of observations from NIRCam given the specified levels
    :param levels:
    :return:
    """
    observations = list()
    page = 1
    initial_request = get_mast_request(
        service=MASTService.FILTERED,
        filters=[get_filter_params(column="obs_collection", values=["JWST"])],
        page=page,
    )
    initial_data = mast_api_request(request_dict=initial_request).json()
    pages = initial_data["paging"]["pagesFiltered"]
    observations.extend(initial_data["data"])
    # iterate over pages
    for page in range(2, pages):
        print(f"On page {page} of {pages}")
        request = get_mast_request(
            service=MASTService.FILTERED,
            filters=[get_filter_params(column="obs_collection", values=["JWST"])],
            page=page,
        )
        result = mast_api_request(request_dict=request).json()
        observations.extend(result["data"])

    return observations


def get_images(observs: List[observations.MastObservation]) -> List[Dict]:
    # get the product list
    obsid_list = [obs.obsid for obs in observs]
    # TODO create a Table from the list of MastObservations
    prod_list = list(Observations.get_product_list(obsid_list))
    return list(map(row_adaptor, prod_list))


if __name__ == "__main__":
    obs: List[Dict] = get_observations()

    #
    # # needs to check for existing observations in DB.
    # # get existing observations in DB - read into set of obsid
    # db.connect()
    # already_synced_obs = observations.MastObservation.select()
    # synced_ids = {synced_obs.obsid for synced_obs in already_synced_obs}
    #
    # # filter list to only include new obsid
    # obs = list(filter(lambda x: x["obsid"] not in synced_ids, obs))
    #
    # with db.atomic():
    #     for idx in range(0, len(obs), 100):
    #         validated: List[schemas.MastObservationBase] = parse_obj_as(
    #             list[schemas.MastObservationBase], obs[idx : idx + 100]
    #         )
    #         values = [
    #             list(validated_obj.dict().values()) for validated_obj in validated
    #         ]
    #         observations.MastObservation.insert_many(values).execute()
    #
    # # Needs to be over new items in DB, not just the returned Observations
    # # get unique obsid in DataProduct
    #
    # # unique_observation_products = observations.DataProduct.select().group_by(observations.DataProduct.observation)
    # # unique_obsIDs = {prod.obsID for prod in unique_observation_products}
    #
    # # get MastObservation with obsid != those from DataProduct
    # new_observations = observations.MastObservation.select().where(
    #     observations.MastObservation.id.not_in(
    #         observations.DataProduct.select().group_by(
    #             observations.DataProduct.observation
    #         )
    #     )
    # )
    # for observ in new_observations:
    #     print(observ)
    #
    # # iterate over MastObservations.
    # prods: List[Dict] = get_images(observs=new_observations)
    # validated_prods = parse_obj_as(list[schemas.DataProductBase], prods)
    # prods_values = [
    #     list(validated_prod.dict().values()).append(
    #         observations.MastObservation.get(
    #             observations.MastObservation.obs_id == validated_prod.obs_id
    #         )
    #     )
    #     for validated_prod in validated_prods
    # ]
    # print(len(prods_values))
    # with db.atomic():
    #     for idx in range(0, len(obs), 100):
    #         observations.DataProduct.insert_many(
    #             prods_values[idx : idx + 100]
    #         ).execute()
    # db.close()
