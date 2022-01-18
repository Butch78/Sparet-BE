from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class LocationBase(SQLModel):
    address: str | None = Field(..., title="Address")
    city: str | None = Field(..., title="City")
    country: str | None = Field(..., title="Country")
    lat: float | None = Field(..., title="Latitude")
    lon: float | None = Field(..., title="Longitude")
    postal_code: str | None = Field(..., title="Postal Code")
    region: str | None = Field(..., title="Region")
    store_number: str | None = Field(..., title="Store Number")


class Location(LocationBase, table=True):
    id: int = Field(default=None, primary_key=True)
    transaction_id: str = Field(
        default=None, title="Transaction Id", foreign_key="transaction.transaction_id"
    )
    transaction: Optional["Transaction"] = Relationship(back_populates="location")
