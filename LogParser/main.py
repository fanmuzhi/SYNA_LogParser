#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
from session import SessionManager
from models import DUT
import os
import re

__author__ = '@boqiling'

FILEPATH = "C:/logfiles/Huangpu/"
DBURI = "sqlite:///logfile.db"
EXT = ".csv"


class RegexPattern(object):
    # Labview
    #REGEX_DUT = re.compile(r"(?P<dut_log>Run.*?)(?=(Run\s\d+|$))", re.DOTALL)
    #REGEX_RUNLINE = re.compile(r"Run\s(?P<run_number>\d+),(?P<date>[^,]+),(?P<time>[^,]+),SN\s(?P<sn>\w{12})")
    #REGEX_BINCODE = re.compile(r"(?P<test_result>(Pass|Fail))\s,BinCode(,|\s)*(?P<bin_codes>(\d+,?)+)")
    ##REGEX_SNRCODE = re.compile(r"SNR,+(?P<snr>([-+]?\d+\.?\d*,)+)")
    #REGEX_SNRCODE = re.compile(r"SNR[,|\r\n|\s]+(?P<snr>([-+]?\d+\.?\d*[,|\s])+)")
    #REGEX_BS0 = re.compile(r"(?<=Boot\sSector\s0)(?P<dut_bs0>.*?)(?=(Pass|Fail))", re.DOTALL)

    # C++
    #REGEX_DUT = re.compile(r"(?P<dut_log>Run.*?)(?=(Run\s\d+|$))", re.DOTALL)
    REGEX_TIME = re.compile(r"(Run\s|Test\sTime),(?P<time>[^\r\n]+)")
    REGEX_SN = re.compile(r"Sensor\sSerial\sNumber\s?,(?P<sn>\w{12})")
    #REGEX_BINCODE = re.compile(r"(?P<test_result>(Pass|Fail))\s,BinCode(,|\s)*(?P<bin_codes>(\d+,?)+)")
    REGEX_BINCODE = re.compile(r"Bin\sCodes(,|\s)*(?P<bin_codes>(\d+,?)+)")
    #REGEX_SNRCODE = re.compile(r"SNR,+(?P<snr>([-+]?\d+\.?\d*,)+)")
    REGEX_SNRCODE = re.compile(r"SNR\sTest[^\r\n]+[,|\s]+(?P<snr>([-+]?\d+\.?\d*[,|\s])+)")
    # REGEX_WOF_BOT = re.compile(r"WOF\sZone\s0,+[^\r\n]+[,|\s]+(?P<wof_bot>([-+]?\d+\.?\d*[,|\s])+)")
    # REGEX_WOF_TOP = re.compile(r"WOF\sZone\s1,+[^\r\n]+[,|\s]+(?P<wof_top>([-+]?\d+\.?\d*[,|\s])+)")
    REGEX_WOF_Z0_FD = re.compile(r"WOF\sZone0\s+FingerDown,+[^\r\n]+[,|\s]+(?P<wof_z0_fd>([-+]?\d+\.?\d*[,|\s])+)")
    REGEX_WOF_Z0_FU = re.compile(r"WOF\sZone0\s+FingerUp,+[^\r\n]+[,|\s]+(?P<wof_z0_fu>([-+]?\d+\.?\d*[,|\s])+)")
    REGEX_WOF_Z1_FD = re.compile(r"WOF\sZone1\s+FingerDown,+[^\r\n]+[,|\s]+(?P<wof_z1_fd>([-+]?\d+\.?\d*[,|\s])+)")
    REGEX_WOF_Z1_FU = re.compile(r"WOF\sZone1\s+FingerUp,+[^\r\n]+[,|\s]+(?P<wof_z1_fu>([-+]?\d+\.?\d*[,|\s])+)")
    REGEX_SCMWOF_BOT = re.compile(r"SCM\sBottom\s+[^\r\n]+[,|\s]+(?P<scmwof_bot>([-+]?\d+\.?\d*[,|\s])+)")
    REGEX_SCMWOF_TOP = re.compile(r"SCM\sTop\s+[^\r\n]+[,|\s]+(?P<scmwof_top>([-+]?\d+\.?\d*[,|\s])+)")
    #REGEX_BS0 = re.compile(r"(?<=Boot\sSector\s0)(?P<dut_bs0>.*?)(?=(Pass|Fail))", re.DOTALL)

    regex_single = [
        REGEX_TIME,
        REGEX_SN,
        REGEX_BINCODE,
        REGEX_SNRCODE,
        REGEX_WOF_Z0_FD,
        REGEX_WOF_Z0_FU,
        REGEX_WOF_Z1_FD,
        REGEX_WOF_Z1_FU,
        REGEX_SCMWOF_BOT,
        REGEX_SCMWOF_TOP,
    ]


def get_files(path, extension):
    """ Get the file in the path with the specified extension
    """
    for root, direct, files in os.walk(path):
        for f in files:
            filename, ext = os.path.splitext(f)
            if ext.upper() == extension.upper():
                yield os.path.join(root, f)


def get_data(filepath):
    """ Get dut dictionary from the specified filepath
    """
    # for csv in get_files(r"C:\logfiles\process", "csv"):
    csv_log = open(filepath, 'rb')
    csv_log_strip = ""
    for line in csv_log.readlines():
        # csv_log_strip += line.strip()   # remove  \r\n or \r or \n
        csv_log_strip += line

    #print csv_log_strip
    csv_log.close()

    #dut_log_list = RegexPattern.REGEX_DUT.findall(csv_log_strip)
    #for dut_log, x in dut_log_list:
    dut = {}
    for pattern in RegexPattern.regex_single:
        r = pattern.search(csv_log_strip)
        if r:
            dut.update(r.groupdict())
            #print r.groupdict();
            #for k, v in r.groupdict():
            #    print k, v
            #    setattr(dut, k, v)
        else:
            print "no found."

        #r = RegexPattern.REGEX_BS0.search(dut_log)
        #if r:
        #    strBS0 = r.group()
        #    print strBS0.strip()
        #else:
        #    print "BS0 not found."

        #yield dut
    return dut


def main():
    sm = SessionManager()
    session = sm.get_session(DBURI)
    sm.prepare_db(DBURI, [DUT])

    for csv in get_files(FILEPATH, EXT):
        print csv
        #for dut_dict in get_data(csv):
        dut_dict = get_data(csv)
        print dut_dict
        dut = DUT()
        for k, v in dut_dict.items():
            setattr(dut, k, v)
        snr_overall = ''
        if dut.snr != None:
            snr_overall = dut.snr.split(',')[-2]

        dut.snr_overall = snr_overall
        bin_code = ''
        if dut.bin_codes != None:
            bin_code = dut.bin_codes.split(',')[0]
            if bin_code != '1':
                dut.test_result = 'Fail'
            else:
                dut.test_result = 'Pass'
        dut.bin_code = bin_code

        # if dut.wof_bot != None:
        #     # dut.wof_bot = dut.wof_bot.strip()
        #     dut.wof_bot_nf, dut.wof_bot_wf, dut.wof_bot_gain, dut.wof_bot_gap = dut.wof_bot.split(',')
        #
        # if dut.wof_top != None:
        #     # dut.wof_top = dut.wof_top.strip()
        #     dut.wof_top_nf, dut.wof_top_wf, dut.wof_top_gain, dut.wof_top_gap = dut.wof_top.split(',')
        if dut.wof_z0_fd != None:
            dut.wof_z0_fd = dut.wof_z0_fd.strip()

        if dut.wof_z0_fu != None:
            dut.wof_z0_fu = dut.wof_z0_fu.strip()

        if dut.wof_z1_fd != None:
            dut.wof_z1_fd = dut.wof_z1_fd.strip()

        if dut.wof_z1_fu != None:
            dut.wof_z1_fu = dut.wof_z1_fu.strip()

        if dut.scmwof_bot != None:
            dut.scmwof_bot = dut.scmwof_bot.strip()
            # dut.scmwof_bot_nf, dut.scmwof_bot_wf, dut.scmwof_bot_gain, dut.scmwof_bot_gap = dut.scmwof_bot.split(',')

        if dut.scmwof_top != None:
            dut.scmwof_top = dut.scmwof_top.strip()
            # dut.scmwof_top_nf, dut.scmwof_top_wf, dut.scmwof_top_gain, dut.scmwof_top_gap = dut.scmwof_top.split(',')


        session.add(dut)
        session.commit()

    session.close()


if __name__ == "__main__":
    main()
