#!/usr/bin/env python
# encoding: utf-8

import csv
from session import SessionManager
from models import DUT
import os
import re

__author__ = 'boqiling'

FILEPATH = "C:/logfiles/process/"
DBURI = "sqlite:///logfile.db"
EXT = ".csv"


class RegexPattern(object):
    REGEX_DUT = re.compile(r"(?P<dut_log>Run\s\d+,.*?)(Run\s\d+,|$)")
    REGEX_RUNLINE = re.compile(r"Run\s(?P<run_number>\d+),(?P<date>[^,]+),(?P<time>[^,]+),SN\s(?P<sn>\w+)")
    REGEX_BINCODE = re.compile(r"(?P<test_result>(Pass|Fail))\s,BinCode,+(?P<bin_codes>(\d,+)?)")
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
    print csv_log_strip

    dut_log_list = RegexPattern.REGEX_DUT.findall(csv_log_strip)
    for dut_log in dut_log_list:
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

    with open('./output.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if(len(row)>1):
                dut = DUT()
                dut.sn = row[0]
                dut.test_result = row[1]
                dut.bin_codes = row[2]
                dut.date = row[3].split(' ')[0]
                if(len(row)>5):
                    dut.snr = row[6]
                session.add(dut)
                session.commit()

#    for csv in get_files(FILEPATH, EXT):
#        for dut_dict in get_data(csv):
#            print dut_dict
#            dut = DUT()
#            for k, v in dut_dict.items():
#                setattr(dut, k, v)
#            print dut.sn
#            session.add(dut)
#            session.commit()
#
    session.close()


if __name__ == "__main__":
    main()
