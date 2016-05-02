#!/usr/bin/env python
# encoding: utf-8

__author__ = 'boqiling'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean

SQLBase = declarative_base()

class DUT(SQLBase):
    __tablename__ = "dut"

    id = Column(Integer, primary_key=True)
    sn = Column(String(20), nullable=True)
    test_result = Column(String(20))
    bin_code = Column(String(10))
    bin_codes = Column(String(20))
    #date = Column(String(20))
    time = Column(String(20))
    snr = Column(String(20))
    snr_total = Column(String(10))
    wof = Column(String(20))
    wof_nf = Column(String(10))
    wof_wf = Column(String(10))
    wof_gap = Column(String(10))
    scmwof = Column(String(20))
    scmwof_nf = Column(String(10))
    scmwof_wf = Column(String(10))
    scmwof_gap = Column(String(10))


    def to_dict(self):
        return {"serial_number": self.sn,
                "bin_code": self.bincode,
                "test_result": self.testresult}
