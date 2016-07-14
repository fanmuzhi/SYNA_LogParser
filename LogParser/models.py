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
    test_result = Column(String(10))
    bin_code = Column(String(10))
    bin_codes = Column(String(30))
    #date = Column(String(20))
    time = Column(String(20))
    # snr = Column(String(20))
    snr_overall = Column(Float(10))
    wof_z0_fd_nf = Column(Integer(5))
    wof_z0_fd_wf = Column(Integer(5))
    wof_z0_fd_gain = Column(Integer(5))
    wof_z0_fd_delta = Column(Integer(5))
    wof_z1_fd_nf = Column(Integer(5))
    wof_z1_fd_wf = Column(Integer(5))
    wof_z1_fd_gain = Column(Integer(5))
    wof_z1_fd_delta = Column(Integer(5))
    wof_z0_fu_nf = Column(Integer(5))
    wof_z0_fu_wf = Column(Integer(5))
    wof_z0_fu_gain = Column(Integer(5))
    wof_z0_fu_delta = Column(Integer(5))
    wof_z1_fu_nf = Column(Integer(5))
    wof_z1_fu_wf = Column(Integer(5))
    wof_z1_fu_gain = Column(Integer(5))
    wof_z1_fu_delta = Column(Integer(5))
    # wof_z0_fu = Column(String(20))
    # wof_z1_fd = Column(String(20))
    # wof_z1_fu = Column(String(20))

    # scmwof_bot = Column(String(20))
    scmwof_bot_nf = Column(Integer(5))
    scmwof_bot_wf = Column(Integer(5))
    scmwof_bot_gain = Column(Integer(5))
    scmwof_bot_delta = Column(Integer(5))
    # scmwof_top = Column(String(20))
    scmwof_top_nf = Column(Integer(5))
    scmwof_top_wf = Column(Integer(5))
    scmwof_top_gain = Column(Integer(5))
    scmwof_top_delta = Column(Integer(5))
    snr = Column(String(50))


    def to_dict(self):
        return {"serial_number": self.sn,
                "bin_code": self.bincode,
                "test_result": self.testresult}
