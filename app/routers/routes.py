from fastapi import APIRouter, Request
from app.extensions import templates
from fastapi.responses import HTMLResponse
from fastapi import Path, Form, Query
from fastapi.responses import RedirectResponse, Response
from dataclasses import dataclass, field
from typing import List
from restcountries import RestCountryApiV2 as rapi

import requests
import json

router = APIRouter()


@router.get("/submit_form", response_class=HTMLResponse)
async def submit_form(request: Request, country: str = Query(...)):

    country_list = rapi.get_countries_by_name(country)

    name_country = country_list[0]

    print(name_country.name)
    print(name_country.currencies[0]["name"])
    print(name_country.capital)
    print(name_country.subregion)
    print(name_country.region)
    print(len(name_country.translations))
    print(name_country.native_name)
    info_country = {
        "img_flag": name_country["flag"],
        "currency": name_country.currencies[0]["name"],
        "capital": name_country.capital,
        "subregion": name_country.subregion,
        "region": name_country.region,
        "translations": name_country.translations,
        "native_name": name_country.native_name,
    }
    return templates.TemplateResponse(
        "single_country.html", {"request": request, "country": country},
    )


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):

    return templates.TemplateResponse(
        "homepage.html", {"request": request, "title": "Home Page"}
    )


@router.get("/index_redirect", response_class=Response)
async def index_redirect():
    response = RedirectResponse(url="/")
    return response


@dataclass
class CountryList:
    endpoint: str = field(init=False, default="https://restcountries.eu/rest/v2")
    region: str = field(init=False, default="region")
    name_region: str
    country_lists: List = field(init=False)

    def __post_init__(self):
        self.country_lists = self.get_country_list(
            self.endpoint, self.region, self.name_region
        )

    def get_country_list(self, endpoint, region, name_region) -> List:
        r = requests.get(f"{endpoint}/{region}/{name_region}")
        country = r.json()

        return country


@router.get("/country/{name}", response_class=HTMLResponse)
async def region(request: Request, name: str = Path(...)):

    country_list = CountryList(name)
    number_of_countries = len(country_list.country_lists)
    list_of_country = country_list.country_lists

    # result = json.dumps(country_list.country_lists, ensure_ascii=False, indent=4)
    # print(result)

    return templates.TemplateResponse(
        "region.html",
        {
            "request": request,
            "title": name,
            "num_of_countries": number_of_countries,
            "list_of_country": list_of_country,
        },
    )

