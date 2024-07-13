import os

"""
Loads the files into a list of subjects ('biology', ...), but each subject contains
a list of topics, ie
[
    {
        'subject': 'biology',
        'topics': ['1.1', '1.2 to 1.4', ....]
    },
    {
        'subject': 'maths',
        'topics': ['1.1', '1.2 to 1.4', ....]
    },
]
It does this by reading through and processing the setup_data/1HR files directory
"""

def load_topics(file_path):

    result = []
    with open(file_path, 'r') as file:
        for topic in file:
            result.append(topic.strip())
    
    return result

def load_files(path="setup_data/1Hr Files") -> list:

    result = {}

    dir_list = os.listdir(path)

    for filename in dir_list:

        filename_noend = filename.replace('.txt','').strip()

        result[filename_noend] = load_topics(path + '//' + filename)

    return result

if __name__=="__main__":

    result = load_files()

    print(result)

