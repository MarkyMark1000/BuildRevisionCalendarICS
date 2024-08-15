import datetime as dt
import os
from dataclasses import dataclass

from .DateSteps import C_DATESTEPS


@dataclass
class topic:
    """Dataclass to represent a topic."""

    description: str
    timedelta_key: str
    timedelta: dt.timedelta


@dataclass
class subject:
    """Dataclass to represent a subject."""

    name: str
    topics: list[topic]
    current_topic: int = 0


class subject_loader:
    """Load subject with topics from file."""

    def _load_topics(self, path: str) -> list[topic]:
        """This is easy to mock in the tests."""
        result = []
        with open(path, "r") as file:
            for row in file:

                str_topic = row.strip()
                td_key = tuple(C_DATESTEPS.keys())[0]
                td = C_DATESTEPS[td_key]

                data = str_topic.split(",")

                if len(data) > 1:
                    if data[1].strip() not in C_DATESTEPS.keys():
                        raise Exception(f"Unrecognised key: {data[1]}")
                    else:
                        str_topic = data[0].strip()
                        td_key = data[1].strip()
                        td = C_DATESTEPS[td_key]

                objTopic = topic(description=str_topic, timedelta_key=td_key, timedelta=td)
                result.append(objTopic)

        return result

    def load(self, name: str, path: str) -> subject:
        """Load subject with topics from file."""
        topics = self._load_topics(path)

        return subject(name=name, topics=topics)


class subjects_loader:
    """Load all subjects corresponding topics in a directory."""

    _subject_loader: subject_loader

    def __init__(self, loader: subject_loader):

        self._subject_loader = loader

    def load(self, directory_path: str) -> list[subject]:
        """Load all subjects corresponding topics in a directory."""
        result = []

        dir_list = os.listdir(directory_path)

        for filename in dir_list:

            filename_noend = filename.replace(".txt", "").strip()

            file_path = directory_path + "//" + filename

            subject = self._subject_loader.load(name=filename_noend, path=file_path)

            result.append(subject)

        return result
