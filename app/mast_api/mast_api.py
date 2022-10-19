import json
from enum import Enum
from typing import Dict, List

import requests

base_url = "https://mast.stsci.edu/api/v0/invoke"


"""
Result Dataset Formats
{
"status" : "EXECUTING|COMPLETE|ERROR",
"msg" : "message string",
"percent complete": percentComplete,
"paging": {'page': currPage, 'pageSize': pagesize, 'pagesFiltered': totPages, 'rows': rowsReturned, 'rowsFiltered': totRows, 'rowsTotal': totRows},
"fields": [
          {"name":"column1 name","type":"column1 datatype"},
          {"name":"column2 name","type":"column2 datatype"},
          ...
          ]
"data" : [
         {"column1 name": "row 1 col 1 value", "column2 name": "row 1 col 2 value",…},
         {"column1 name": "row 2 col 1 value", "column2 name": "row 2 col 2 value",…},
         ...
         ]
}
"""


class MASTService(Enum):
    FILTERED = "Mast.Caom.Filtered"
    PRODUCTS = "Mast.Caom.Products"
    NIRCAM = "Mast.Jwst.Filtered.Nircam"
    NIRISS = "Mast.Jwst.Filtered.Niriss"
    NIRSPEC = "Mast.Jwst.Filtered.Nirspec"
    MIRI = "Mast.Jwst.Filtered.Miri"
    FGS = "Mast.Jwst.Filtered.Fgs"
    GUIDESTAR = "Mast.Jwst.Filtered.GuideStar"
    WSS = "Mast.Jwst.Filtered.Wss"


# for reference - from https://mast.stsci.edu/api/v0/pyex.html
def download_request(payload, filename, download_type="file"):
    request_url = "https://mast.stsci.edu/api/v0.1/Download/" + download_type
    resp = requests.post(request_url, data=payload)

    with open(filename, "wb") as f:
        f.write(resp.content)

    return filename


def mast_api_request(request_dict):
    # url
    base_url = "https://mast.stsci.edu/api/v0/invoke"

    # construct the request - headers are mandatory
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    # make the request
    res = requests.post(
        url=base_url, data=f"request={json.dumps(request_dict)}", headers=headers
    )
    return res


def get_mast_request(
    service: MASTService,
    filters: List[Dict] = None,
    filename: str = None,
    page: int = 1,
    page_size: int = 1000,
    timeout: int = 20,
) -> Dict:
    mast_request = {
        "service": service.value,
        "params": {
            "columns": "*",  # this means all columns
            "filters": filters if filters is not None else list(),
        },  # see https://mast.stsci.edu/api/v0/_services.html
        "format": "json",
        "page": page,
        "pagesize": page_size,
        "timeout": timeout,
    }
    if filename is not None:
        mast_request["filename"] = filename
    return mast_request


def get_filter_params(
    column: str, values: List = None, separator: str = None, search_text: str = None
) -> Dict:
    """
    Constructor for jwst filter params.
    :param column: String The column name to be filtered
    :param values: Optional List Acceptable values or range in the form
        [{"min": min_value, "max": max_value}].
    :param separator: Optional String Separator for multivalued columns (eg region?)
    :param search_text: Optional String A search term (can use wildcard character %)
    :return:
    """
    filter_dict = {
        "paramName": column,
        "values": values if values is not None else list(),
    }
    if separator is not None:
        filter_dict["separator"] = separator
    if search_text is not None:
        filter_dict["freeText"] = search_text
    return filter_dict


if __name__ == "__main__":
    jwst_filter = get_filter_params(column="obs_collection", values=["JWST"])
    products_request = get_mast_request(
        service=MASTService.FILTERED,
        filters=[jwst_filter],
    )
    products_data = mast_api_request(request_dict=products_request)
    print(products_data.json())
