import datetime as dt

C_LOGGING = False

# No revision before this hour on a school day:
C_SCHOOLDAY_CUTOFF_HOUR = 18

# Current and 1 Hr are done by default
C_DATESTEPS = {
    "1 day": dt.timedelta(days=1),
    "1 week": dt.timedelta(days=7),
    "1 month": dt.timedelta(days=28),
    "3 month": dt.timedelta(days=84),
    "6 month": dt.timedelta(days=168),
}
