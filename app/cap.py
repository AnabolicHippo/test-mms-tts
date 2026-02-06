from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CAPInfo(BaseModel):
    category: Optional[List[str]] = Field(
        default=None,
        description="CAP category codes such as Geo, Met, Safety, Security.",
    )
    event: Optional[str] = Field(default=None, description="CAP event name.")
    urgency: Optional[str] = Field(default=None, description="Immediate, Expected, Future.")
    severity: Optional[str] = Field(default=None, description="Extreme, Severe, Moderate.")
    certainty: Optional[str] = Field(default=None, description="Observed, Likely, Possible.")
    headline: Optional[str] = Field(default=None, description="Short public alert headline.")
    description: Optional[str] = Field(default=None, description="Expanded alert description.")
    instruction: Optional[str] = Field(default=None, description="Recommended actions.")
    language: Optional[str] = Field(default=None, description="Language tag for the info block.")


class CAPAlert(BaseModel):
    identifier: Optional[str] = Field(default=None, description="Unique ID for the alert.")
    sender: Optional[str] = Field(default=None, description="Originating sender.")
    sent: Optional[datetime] = Field(default=None, description="Timestamp the alert was sent.")
    status: Optional[str] = Field(default=None, description="Actual, Exercise, Test, Draft.")
    msg_type: Optional[str] = Field(default=None, alias="msgType")
    scope: Optional[str] = Field(default=None, description="Public, Restricted, Private.")
    info: Optional[CAPInfo] = Field(default=None, description="Information block.")
