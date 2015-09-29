#!/usr/bin/env python
# encoding: utf-8

__author__ = 'boqiling'

import csv
from session import SessionManager
from models import DUT

dburi = "sqlite:///test.db"


def main():
    sm = SessionManager()
    session = sm.get_session(dburi)
    sm.prepare_db(dburi, [DUT])

    with open('./output.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if(len(row)>1):
                dut = DUT()
                dut.serialnumber = row[0]
                dut.testresult = row[1]
                dut.bincode = row[2]
                dut.testdate = row[3].split(' ')[0]
                if(len(row)>5):
                    dut.snr = row[6]

                session.add(dut)
                session.commit()
    session.close()


if __name__ == "__main__":
    main()


