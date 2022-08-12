# Representation of Dates and Times - ISO 8601 Format

## History

- ISO 8601:1988
- ISO 8601:2000
- ISO 8601:2004
- ISO 8601-1:2019
- ISO 8601-2:2019

## Year

```plaintext
YYYY  # eg. 2022

# `+`: AD = Anno Domini (公元)
# `-`: BC = Before Christ (公元前)
±YYYYY  # eg. +2022
```

## Calendar Date

Use **Gregorian calendar**.

```plaintext
YYYY-MM-DD or YYYYMMDD  # eg. 2022-01-01 or 20220101

YYYY-MM (but not YYYYMM)  # eg. 2022-01
```

## Week Date

```plaintext
YYYY-Www or YYYYWww  # eg. 2022-W01 or 2022W01

# D = [1-7], Monday to Sunday
YYYY-Www-D or YYYYWwwD  # eg. 2022-W01-1 or 2022W011
```

There are several mutually equivalent and compatible descriptions of week 01:

- the week with the first business day in the starting year
(considering that Saturdays, Sundays and 1st January are non-working days),
- the week with the starting year's first Thursday in it (the formal ISO definition),
- the week with 4 January in it,
- the first week with the majority (four or more) of its days in the starting year, and
- the week starting with the Monday in the period 29 December - 4 January.

## Ordinal Date

```plaintext
# DDD = [001-365] (366 in leap years).
YYYY-DDD or YYYYDDD  # eg. 2022-365 or 2022365
```

## Time

```plaintext
# 'T': ISO 8601-1:2019 introduced
# 'hh' = [00-23]
# 'mm' = [00-59]
# 'ss' = [00-59], 60 for denoting an added leap second
# As of ISO 8601-1:2019 midnight may only be referred to as "00:00",
# Earlier versions of the standard allowed "24:00" corresponding to the end of a
#   day, but this is explicitly disallowed by the 2019 revision.

hh:mm:ss.sss or Thhmmss.sss  # eg. 12:00:00.123 or T120000.123

hh:mm:ss or Thhmmss  # eg. 12:00:00 or T120000

hh:mm or Thhmm  # eg. 12:00 or T1200

Thh  # eg. T12
```

## Time Zone Designators

### Local time (unqualified)

```plaintext
TIME  # eg. 14:45:15
```

### Coordinated Universal Time (UTC)

The **'Z'** suffix in the ISO 8601 time representation is sometimes referred to as
"*Zulu time*" because the same letter is used to designate the *Zulu time zone*.

```plaintext
TIMEZ  # eg. 14:45:15Z
```

### Time offsets from UTC

```plaintext
"−05:00" for New York on standard time (UTC-05:00)
"−04:00" for New York on daylight saving time (UTC-04:00)
"+00:00" (but not "−00:00") for London on standard time (UTC±00:00)
"+02:00" for Cairo (UTC+02:00)
"+05:30" for Mumbai (UTC+05:30)
"+08:00" for China (UTC+08:00)
"+14:00" for Kiribati (UTC+14:00)
```

## Combined date and time

```plaintext
DATETTIME  # eg. 2022-01-02T14:30

DATETTIMEZ  # eg. 2007-04-05T14:30Z
```

## Durations

```plaintext
# 'P': duration designator (for period)
# 'Y': year designator
# 'M': month designator
# 'D': day designator
# 'T': time designator
# 'H': hour designator
# 'M': minute designator
# 'S': second designator

PnYnMnDTnHnMnS  # eg. P3Y2M1DT10H0M0S = 3 years, 2 months, 1 day and 10 hours, ...

PnW  # eg. P1W = one week
```

## Time Interval

```plaintext
STARTTIME/ENDTIME

STARTTIME/DURATION

DURATION/ENDTIME

DURATION

# Recurring time interval
Rn/INTERVAL

R/INTERVAL
```

## Adoption as national standards

- United States: **ANSI INCITS 30-1997** (R2008) and **NIST FIPS PUB 4-2**
- China: **GB/T 7408-2005**

## References

- [Wikipedia - ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
- [ISO 8601-1:2009](https://www.iso.org/obp/ui/#iso:std:iso:8601:-1:ed-1:v1:en)
- [ISO 8601-2:2009](https://www.iso.org/obp/ui/#iso:std:iso:8601:-2:ed-1:v1:en)
