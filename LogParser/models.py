#!/usr/bin/env python
# encoding: utf-8

__author__ = 'boqiling'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean

SQLBase = declarative_base()

class DUT(SQLBase):
    __tablename__ = "dut"

    id = Column(Integer, primary_key=True)
    serialnumber = Column(String(20), nullable=False)
    testresult = Column(String(20))
    bincode = Column(String(20))
    testdate = Column(String(20))
    snr = Column(String(20))

    def to_dict(self):
        return {"serial_number": self.serialnumber,
                "bin_code": self.bincode,
                "test_result": self.testresult}
