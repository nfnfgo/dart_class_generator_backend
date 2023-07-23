# Fundamentals
from typing import Annotated

# FastAPI
from fastapi import APIRouter, Depends, Query, Body

# generator package
import dart_class_gen as dartgen

# models
from models.query import DartGenQueryInfo
from models.response import DartClassGenResInfo

router: APIRouter = APIRouter()


@router.post("/", response_model=DartClassGenResInfo)
def generate_dart_class(gen_info_query: Annotated[DartGenQueryInfo, Body()]):
    res_str: str | None = dartgen.data_model_generator.generate(
        gen_info=gen_info_query.to_gen_class()
    )
    return DartClassGenResInfo().set_res(res_str)
