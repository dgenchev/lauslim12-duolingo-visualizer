from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class Summary(BaseSchema):
    date: str = Field(alias="date")
    gained_xp: Optional[int] = Field(alias="gainedXp", default=None)
    num_sessions: Optional[int] = Field(alias="numSessions", default=None)
    total_session_time: Optional[int] = Field(alias="totalSessionTime", default=None)

    @field_validator("date", mode="before")
    @classmethod
    def unix_timestamp_transform(cls, raw: int | str) -> str:
        return (
            raw
            if isinstance(raw, str)
            else datetime.fromtimestamp(raw).strftime("%Y/%m/%d")
        )

    @model_validator(mode='after')
    def convert_none_to_zero(self) -> 'Summary':
        """Convert None values to 0 for fields that should be integers"""
        if self.gained_xp is None:
            self.gained_xp = 0
        if self.num_sessions is None:
            self.num_sessions = 0
        if self.total_session_time is None:
            self.total_session_time = 0
        return self

    @staticmethod
    def create_default(date: str) -> "Summary":
        return Summary(
            date=date,
            gainedXp=0,
            numSessions=0,
            totalSessionTime=0,
        )


class User(BaseSchema):
    site_streak: int = Field(alias="siteStreak")


class DatabaseEntry(BaseSchema):
    xp_today: int
    number_of_sessions: int
    session_time: int
    streak: int

    @staticmethod
    def create(summary: Summary, streak: int) -> "DatabaseEntry":
        return DatabaseEntry(
            xp_today=summary.gained_xp,
            number_of_sessions=summary.num_sessions,
            session_time=summary.total_session_time,
            streak=streak,
        )

    @staticmethod
    def create_default(streak: int) -> "DatabaseEntry":
        return DatabaseEntry(
            xp_today=0,
            number_of_sessions=0,
            session_time=0,
            streak=streak,
        )
