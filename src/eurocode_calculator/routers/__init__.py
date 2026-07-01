"""Routers FastAPI."""

from eurocode_calculator.routers.beam import router as beam_router
from eurocode_calculator.routers.column import router as column_router
from eurocode_calculator.routers.foundation import router as foundation_router
from eurocode_calculator.routers.report import router as report_router

__all__ = ["beam_router", "column_router", "foundation_router", "report_router"]
