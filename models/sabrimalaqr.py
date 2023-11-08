from pydantic import BaseModel
from typing import List

class ClsQR:
    class ClsSabarimalaQr(BaseModel):
        PassNos: List[str] = []
        JourneyDate: str = ""
        ValidTill: str = ""
        CustomerName: str = "" 
        CustomerMobile: str = ""
        FromCity: str = ""
        ToCity: str = ""
        PassType: str = ""

        def __repr__(self):
            return f"{','.join([str(elem) for elem in self.PassNos])}|{self.JourneyDate}|{self.ValidTill}|{self.CustomerName}|{self.CustomerMobile}|{self.FromCity}|{self.ToCity}|{self.PassType}" 