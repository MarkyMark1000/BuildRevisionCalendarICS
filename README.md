# REVISION CALENDAR ICS
---

This is for building a revision calendar for the kids to help with their
revision timetable.

## CONFIGURATION
---

These sources were used for the basis of our configuration files:

.flake8 and pyproject.toml:
https://www.mindee.com/blog/python-coding-practices

## PYTHON
---

Initite a python virtual environment and install the requirements file
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

There is a make file that can be used to run a number of commands

To clean up the code, consider:
```
black .
make isort
make flake8
```

To run the code to build the calender:
```
python3 create_calender.py
```

## BUILD A CALENDAR
---

### Control Files:
These are used by the datetime checkers to see if a date is invalid, within a school holiday
and and invalid weekday/hour within or outside of the school holidays.   Update these files
when you start revising for a new academic school year.

### 1Hr Files:
Each file represents a subject and contains a list of topics that can be revised within a
1 hour time period (ideally 50 minutes).   Add or update these files as necessary before
building a new calendar.   You should be able to add a second column to the file if you want
to override the default start time of 'now' with something like '1 Hour' or '1 Week'. 

### create_calendar.py:
Adjust the start_datetime at the bottom of the file and then run the code as follows:
```
python3 create_calender.py
```

## CODE STRUCTURE
---

### create_calendar.py

This is the main file 


### HELPERS
---

This is where the majority of the code resides:

#### DateCheckers, DateTransformers and DCTContainer

I have tried to make the checkers and transformers relatively SOLID.   The checkers check the
datetime input to see if it conflicts with a particular requirement.   The Transformers specify
how to adjust the datetime if it conflicts with the requirement.   The DCTContainer is used to
pair up the Checkers with corresponding Transformers and run them all against a particular
input datetime until a valid datetime is found.

#### Subjects and Topics

This code uses dataclasses to load data from the setup_data/1Hr files directory into corresponding
subjects and topics.   This data is then used to build a timeline.

#### DateSteps

This is a class that represents a particular datetime with a label such as 'now' and then steps
forward in time via the corresponding values within C_DATESTEPS, ie '1 Hour', '1 Day', '1 Week'
etc.   It is a helper class.

#### TimeLine

This code uses the other components such as DCTContainer, Subjects, Topics etc to build the
timeline as a dictionary of calendar events.

#### ResultBuilder

This uses the timeline, ie dictionary of calendar events to build the output files within the
/result_data/ directory.

### TESTS
---

This contains all of the unit tests for this project.