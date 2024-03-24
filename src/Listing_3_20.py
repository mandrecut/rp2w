from machine import WDT

wdt = WDT(timeout=5000)
wdt.feed()
