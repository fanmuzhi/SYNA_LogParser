-- select distinct sn from dut
select AVG(snr_total) from dut where dut.bin_code="129"
select DISTINCT(sn) from dut;
select * from `dut` where `sn` in (SELECT distinct(sn) from dut where bin_code = '1') and bin_code ='1' GROUP BY sn;
select * from `dut` where `sn`  not in (SELECT distinct(sn) from dut where bin_code = '1') GROUP BY sn;