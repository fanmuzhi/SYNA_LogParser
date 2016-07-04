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
    snr_overall = Column(String(10))
    # wof_bot = Column(String(20))
    # wof_bot_nf = Column(String(10))
    # wof_bot_wf = Column(String(10))
    # wof_bot_gain = Column(String(10))
    # wof_bot_gap = Column(String(10))
    # wof_top = Column(String(20))
    # wof_top_nf = Column(String(10))
    # wof_top_wf = Column(String(10))
    # wof_top_gain = Column(String(10))
    # wof_top_gap = Column(String(10))
    # scmwof_bot = Column(String(20))
    wof_z0_fd = Column(String(20))
    wof_z0_fu = Column(String(20))
    wof_z1_fd = Column(String(20))
    wof_z1_fu = Column(String(20))

    scmwof_bot = Column(String(20))
    # scmwof_bot_nf = Column(String(10))
    # scmwof_bot_wf = Column(String(10))
    # scmwof_bot_gain = Column(String(10))
    # scmwof_bot_gap = Column(String(10))
    scmwof_top = Column(String(20))
    # scmwof_top_nf = Column(String(10))
    # scmwof_top_wf = Column(String(10))
    # scmwof_top_gain = Column(String(10))
    # scmwof_top_gap = Column(String(10))
    snr = Column(String(20))


    def to_dict(self):
        return {"serial_number": self.sn,
                "bin_code": self.bincode,
                "test_result": self.testresult}
