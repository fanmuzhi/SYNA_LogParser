#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
from session import SessionManager
from models import DUT
import os
import re

__author__ = '@boqiling'

FILEPATH = "C:/logfiles/process/"
DBURI = "sqlite:///logfile.db"
EXT = ".csv"


class RegexPattern(object):
    REGEX_DUT = re.compile(r"(?P<dut_log>Run.*?)(?=(Run\s\d+|$))")
    REGEX_RUNLINE = re.compile(r"Run\s(?P<run_number>\d+),(?P<date>[^,]+),(?P<time>[^,]+),SN\s(?P<sn>\w{12})")
    REGEX_BINCODE = re.compile(r"(?P<test_result>(Pass|Fail))\s,BinCode(,|\s)*(?P<bin_codes>(\d+,?)+)")
    REGEX_SNRCODE = re.compile(r"SNR,+(?P<snr>([-+]?\d+\.?\d*,)+)")

    regex_single = [
        REGEX_RUNLINE,
        REGEX_BINCODE,
        REGEX_SNRCODE,
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
    #for csv in get_files(r"C:\logfiles\process", "csv"):
    csv_log = open(filepath, 'rb')
    csv_log_strip = ""
    for line in csv_log.readlines():
        csv_log_strip += line.strip()   # remove  \r\n or \r or \n

    csv_log.close()

    dut_log_list = RegexPattern.REGEX_DUT.findall(csv_log_strip)
    for dut_log, x in dut_log_list:
        dut = {}
        for pattern in RegexPattern.regex_single:
            r = pattern.search(dut_log)
            if r:
                dut.update(r.groupdict())
                #for k, v in r.groupdict():
                #    print k, v
                #    setattr(dut, k, v)
            else:
                print "no found."
        yield dut


def main():
    sm = SessionManager()
    session = sm.get_session(DBURI)
    sm.prepare_db(DBURI, [DUT])

    for csv in get_files(FILEPATH, EXT):
        print csv
        for dut_dict in get_data(csv):
            print dut_dict
            dut = DUT()
            for k, v in dut_dict.items():
                setattr(dut, k, v)
            print dut.sn
            snr_total = None
            if dut.snr != None:
                snr_total = dut.snr.split(',')[2]

            dut.snr_total = snr_total
            bin_code = None
            if dut.bin_codes != None:
                bin_code = dut.bin_codes.split(',')[0]
            dut.bin_code = bin_code

            session.add(dut)
            session.commit()

    session.close()


if __name__ == "__main__":
    main()
