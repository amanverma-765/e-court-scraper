"""
Pydantic schemas for request and response validation.
"""

from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field, validator


class ErrorResponse(BaseModel):
    """Standard error response model."""
    status: str = "error"
    code: int
    message: str
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    """Standard success response model."""
    status: str = "success"
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


# ===== Authentication Schemas =====

class AuthTokenResponse(SuccessResponse):
    """Response for JWT token generation."""
    data: Dict[str, str] = Field(default=None)


# ===== Case Schemas =====

class CaseDetailRequest(BaseModel):
    """Request model for getting case details by CNR."""
    cnr: str = Field(..., min_length=1, max_length=100, description="Case Number Reference")

    class Config:
        json_schema_extra = {
            "example": {
                "cnr": "UPBL060021142023"
            }
        }


class CaseDetailResponse(SuccessResponse):
    """Response for case details."""
    data: Optional[Dict[str, Any]] = None


# ===== Cause List Related Schemas =====

class StatesResponse(SuccessResponse):
    """Response for states list."""
    data: Optional[Dict[str, Any]] = None


class DistrictsRequest(BaseModel):
    """Request model for getting districts by state."""
    state_code: str = Field(..., min_length=1, description="State code")

    class Config:
        json_schema_extra = {
            "example": {
                "state_code": "5"
            }
        }


class DistrictsResponse(SuccessResponse):
    """Response for districts list."""
    data: Optional[Dict[str, Any]] = None


class CourtComplexRequest(BaseModel):
    """Request model for getting court complex."""
    state_code: str = Field(..., min_length=1, description="State code")
    district_code: str = Field(..., min_length=1, description="District code")

    class Config:
        json_schema_extra = {
            "example": {
                "state_code": "5",
                "district_code": "7"
            }
        }


class CourtComplexResponse(SuccessResponse):
    """Response for court complex."""
    data: Optional[Dict[str, Any]] = None


class CourtNameRequest(BaseModel):
    """Request model for getting court names."""
    state_code: str = Field(..., min_length=1, description="State code")
    district_code: str = Field(..., min_length=1, description="District code")
    court_code: str = Field(..., min_length=1, description="Court code")

    class Config:
        json_schema_extra = {
            "example": {
                "state_code": "5",
                "district_code": "7",
                "court_code": "3"
            }
        }


class CourtNameResponse(SuccessResponse):
    """Response for court names."""
    data: Optional[Dict[str, Any]] = None


class CauseListRequest(BaseModel):
    """Request model for getting cause list."""
    state_code: str = Field(..., min_length=1, description="State code")
    district_code: str = Field(..., min_length=1, description="District code")
    court_code: str = Field(..., min_length=1, description="Court code")
    court_number: str = Field(..., min_length=1, description="Court number")
    cause_list_type: str = Field(
        ...,
        description="Type of cause list: 'CIVIL' or 'CRIMINAL'",
        pattern="^(CIVIL|CRIMINAL)$"
    )
    date: str = Field(
        ...,
        description="Date in DD-MM-YYYY format",
        pattern=r"^\d{2}-\d{2}-\d{4}$"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "state_code": "5",
                "district_code": "7",
                "court_code": "1",
                "court_number": "1",
                "cause_list_type": "CIVIL",
                "date": "16-10-2020"
            }
        }


class CauseListResponse(SuccessResponse):
    """Response for cause list."""
    data: Optional[Dict[str, Any]] = None


# ===== Health Check =====

class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    message: str = "API is running"
