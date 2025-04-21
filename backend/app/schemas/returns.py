from pydantic import BaseModel
from typing import Optional
from datetime import date

class ReturnBase(BaseModel):
    order_id: int
    r_shipping_method: Optional[str] = None
    r_tracking_info: Optional[str] = None
    r_date_returned: Optional[date] = None
    r_items_returned: Optional[int] = None
    r_retuned_hub: Optional[bool] = None
    r_return_reason: Optional[str] = None
    r_condition: Optional[str] = None
    r_comments: Optional[str] = None
    r_processed_date: Optional[date] = None
    h_booked_back: Optional[bool] = None
    h_condition: Optional[str] = None
    h_comments: Optional[str] = None
    h_processed_date: Optional[date] = None
    b_billed: Optional[bool] = None
    b_billing_Value: Optional[float] = None

class ReturnCreate(ReturnBase):
    pass

class ReturnUpdate(ReturnBase):
    pass

class ReturnOut(ReturnBase):
    id: int
    class Config:
        orm_mode = True
