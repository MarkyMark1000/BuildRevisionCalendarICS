import os
import datetime as dt
from dataclasses import dataclass
from .constants import C_DATESTEPS

@dataclass
class topic():
    description: str
    timedelta_key: str
    timedelta: dt.timedelta

@dataclass
class subject():
    name: str
    topics: list[topic]

class subject_loader():

    def _get_timedelta(self, timedelta_key):
        
        for k, v in C_DATESTEPS.items():
            if k.upper() == timedelta_key.strip().upper():
                return v
        
        raise Exception(f'Could not find timedelta: {timedelta_key}')

    def _load_topics(self, path: str) -> list[topic]:
        """
        This is easy to mock in the tests
        """
        result = []
        with open(path, "r") as file:
            for row in file:

                str_topic = row.strip()
                data = str_topic.split(",")

                if len(data)<2:
                    td = None
                else:
                    str_topic = data[0]
                    td = self._get_timedelta(data[1])
                
                objTopic = topic(
                    description = str_topic,
                    timedelta_key = data[1],
                    timedelta = td
                )
                result.append(objTopic)

        return result

    def load(self, name: str, path: str) -> subject:
        
        topics = self._load_topics(path)

        return subject(
            name = name,
            topics = topics
        )

class subjects_loader():

    _subject_loader: subject_loader

    def __init__(self, loader: subject_loader):

        self._subject_loader = loader

    def load(self, directory_path: str) -> list[subject]:

        result = []

        dir_list = os.listdir(directory_path)

        for filename in dir_list:

            filename_noend = filename.replace(".txt", "").strip()

            file_path = directory_path + "//" + filename

            subject = self._subject_loader.load(
                name=filename_noend,
                path = file_path
            )

            result.append(subject)

        return result
