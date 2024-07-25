import datetime as dt


class SchoolHolidays:

    _data: list

    def __init__(self, path="setup_data/Control Files/school_holidays.txt"):

        self._data = list()
        with open(path, "r") as file:
            for line in file:
                rdata = line.split(",")
                start_date = rdata[0].strip()
                end_date = rdata[1].strip()
                start_date = dt.datetime.strptime(start_date, "%d-%B-%Y")
                end_date = dt.datetime.strptime(end_date, "%d-%B-%Y").replace(hour=23, minute=59)
                if (end_date - start_date).total_seconds() < 0:
                    raise Exception(f"Invalid Start/End date: {start_date}, {end_date}")
                self._data.append({"start_date": start_date, "end_date": end_date})

    def is_within_school_holiday(self, input_datetime: dt) -> bool:

        ret = False
        for row in self._data:
            if (input_datetime - row["start_date"]).total_seconds() >= 0 and (
                input_datetime - row["start_date"]
            ).total_seconds() <= (row["end_date"] - row["start_date"]).total_seconds():

                ret = True
                break

        return ret
