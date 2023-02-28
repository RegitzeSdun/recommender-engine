import os
import datetime
import pytz
from typing import List, Dict, Tuple
from collections import defaultdict
from fastapi import FastAPI
from fastapi_versioning.versioning import version_to_route
from fastapi.routing import APIRoute
from starlette.routing import Route

from recommender_engine.utils.custom_exceptions import DateParseError


def parse_time(t: str) -> float:
    """Parses a classic corti timestamp to seconds since 0."""
    try:
        return (datetime.datetime.strptime(t, TIME_FORMAT) - REFTIME).total_seconds()
    except ValueError:
        return (
            datetime.datetime.strptime(t, TIME_FORMAT_WITHOUT_MS) - REFTIME
        ).total_seconds()


def parse_date(date: str) -> str:
    """
    Convert from
        "%Y-%m-%d %H:%M:%S"
        " %Y-%m-%d %H:%M:%S "
        "%Y-%m-%d %H:%M:%S.%f"
        "%Y-%m-%d %H:%M:%S.%f000000000000Z"
        "%Y-%m-%dT%H:%M:%S"
    to DATE_FORMAT
        "%Y-%m-%dT%H:%M:%S.%f"
    and validate date string for errors
    """
    date = date.strip().replace("Z", "")
    if "T" in DATE_FORMAT and "T" not in date:
        date = date.replace(" ", "T")
    if "." in DATE_FORMAT and "." not in date:
        date += ".000000"
    date = date.ljust(26, "0") if len(date) <= 26 else date[:26]
    try:
        datetime.datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        raise DateParseError(
            f"Date string '{date}' doesn't match expected format: '{DATE_FORMAT}'"
        )
    return date


def add_absolute_date_and_match_time(
    call_absolute_date: str, match_time: float
) -> datetime.datetime:
    return (
        datetime.datetime.strptime(
            call_absolute_date,
            "%Y-%m-%dT%H:%M:%S.%f",
        )
        + datetime.timedelta(seconds=match_time)
    ).replace(tzinfo=pytz.UTC)


def get_api_version() -> int:
    return int(os.environ["API_VERSION"])


def create_routers_with_versions(app: FastAPI, major_version: int) -> Dict[str, Route]:
    """
    Create routers with version name before endpoint path. e.g. /search -> /v1/search
    :param app: Fast API instantiated app
    :param major_version: Major version of the API
    :return: Dictionary contains new path and router {"path|Method": APIRoute}
    """
    # Placeholder with types for later use
    routers_with_versions: Dict[str, Route] = defaultdict()
    version_route_mapping: Dict[Tuple[int, int], List[APIRoute]] = defaultdict(list)
    prefix_format: str = "/v{major}"

    # Creat tuple as (major, minor) and add them to each router
    # Setting the second argument of Tuple to 0  for minor version
    version_routers = [
        version_to_route(router, (major_version, 0)) for router in app.routes
    ]
    for version, router in version_routers:
        version_route_mapping[version].append(router)

    # Add version to each endpoint path
    for version in version_route_mapping.keys():
        major, _ = version
        # Create prefix from version
        prefix = prefix_format.format(major=major)
        for route in version_route_mapping[version]:
            # Create path with version and add method
            for method in route.methods:
                route.path_format = f"{prefix}{route.path}"
                routers_with_versions[route.path + "|" + method] = route
    return routers_with_versions


def find_match_sentence_indexes(text_with_tag: str) -> List[dict]:
    """
    From space separated texts with <b> tags around the search terms,
    returns the indexes of the search terms.
    :param text_with_tag: Row text with search term tags
    :return: List of indexes in dictionary [{"start": 1, "stop": 2}]
    """
    # Find all indexes begin with <b> (search term matches)
    search_term_indexes = [
        index
        for index, word in enumerate(text_with_tag.split())
        if word.startswith("<b>")
    ]

    # If no match, return empty list
    if not search_term_indexes:
        return []

    # Iterate over search term indexes, add start and stop index of the concurrent numbers to the list
    index_list = []
    one_search_term_index = {"start": search_term_indexes[0]}
    previous_index = search_term_indexes[0]
    for index in search_term_indexes[1:]:
        if index != previous_index + 1:
            one_search_term_index["stop"] = previous_index
            index_list.append(one_search_term_index)
            one_search_term_index = {"start": index}
        previous_index = index

    # Add final stop to the index list
    one_search_term_index["stop"] = previous_index
    index_list.append(one_search_term_index)
    return index_list
