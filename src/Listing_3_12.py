from machine import RTC

rtc = RTC()
rtc.datetime((2024, 1, 23, 1, 12, 48, 0, 0))
print(rtc.datetime()) 

