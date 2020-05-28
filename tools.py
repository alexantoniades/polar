import json, os, re
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from numpy import asarray
# Disable TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#----------------------------------[ Struct class ]--------------------------------------#
class Struct:
    """C Struct-like class"""
    def __init__(self, **entries):
        self.__dict__.update(entries)
#------------------------------[ Import JSON function ]----------------------------------#
def importJSON(path_to_json) -> dict:
    """Imports JSON file and returns a dictionary"""
    try:
        with open(path_to_json, 'r') as f:
            json_data = json.load(f)
        return(json_data)
    except Exception as error:
        print(f"Error: importJSON({path_to_json}) -> {error}")
#------------------------------[ Export JSON function ]----------------------------------#
def exportJSON(data, path_to_json="./exported_data.json") -> None:
    """Exports a dictionary to JSON file"""
    try:
        with open(path_to_json, 'w') as f:
            return(json.dump(data, f))
    except Exception as error:
        print(f"Error: exportJSON({path_to_json}) -> {error}")
#-------------------------------[ Occurrences class ]------------------------------------#
class Occurrences:
    """A class for creating, storing and finding word occurrences"""
    def __init__(self, vocabulary=[], users={}, blacklist=[]):
        self.vocabulary = vocabulary
        self.users = users
        self.blacklist = blacklist
        if users == {}:
            self.users = self.fromJSON('./data/users.json')
        if vocabulary == []:
            self.index = self.fromJSON('./data/occurrences.json')
        else:    
            self.index = self.create_index(vocabulary)
        if self.blacklist == []:
            self.blacklist = self.fromJSON('./data/blacklist.json')

    def create_index(self, vocabulary=[]) -> dict:
        """Creates dictionary of occurrences"""
        try:
            out = {}
            for word in vocabulary:
                if word in out:
                    out[word] += 1
                else: 
                    out[word] = 1
            return(out)
        except Exception as error:
            print(f"Error: self.create_index([...]) -> {error}")

    @property
    def total(self) -> int:
        """Returns total occurrences"""
        total = 0
        for item in self.index:
            total += self.index[item]
        return(total)

    def query(self, target):
        """Returns index key or value depending on the parameter type"""
        try:
            if type(target) is int:
                for key, value in self.index.items():
                    if value == target:
                        return(key)
            elif type(target) is str:
                for key, value in self.index.items():
                    if key == target:
                        return(value)
        except Exception as error:
            print(f"Error: self.query({target}) -> {error}")

    def exists(self, string) -> bool:
        """Checks if string exists in index"""
        if string in self.index:
            return(True)
        else:
            return(False)

    def find(self, string) -> int:
        """Returns strings occurrences in index"""
        if not self.exists(string):
            self.index[string] = 0
        return(self.index[string])

    def ratio(self, string='') -> float:
        """Returns ratio of strig occurrence over total occurrences"""
        try:
            return(self.find(string)/self.total)
        except Exception as error:
            print(f"Error: self.ratio({string}) -> {error}")

    def sentence(self, string='') -> float:
        """Returns average float occurrence of sentence"""
        try:
            out = 0
            for word in string.split(' '):
                out += self.ratio(word)
            return(out)
        except Exception as error:
            print(f"Error: self.sentence({string}) -> {error}")

    def is_user(self, user='') -> int:
        """Returns 1 of user ID exists in user index, if not then 0"""
        try:
            if user in self.users:
                return(1)
            else:
                return(0)
        except Exception as error:
            print(f"Error: self.is_user({user}) -> {error}")

    def is_blacklisted(self, string='') -> int:
        """Returns 1 of command exists in blacklist, if not then 0"""
        try:
            for word in string.split(' '):
                if word in self.blacklist:
                    return(1)
                else:
                    return(0)
        except Exception as error:
            print(f"Error: self.is_blacklisted({string}) -> {error}")

    def encode(self, command, user) -> list:
        """Returns list of command average ratio, 1 if user is valid and 1 if any command is in blacklist"""
        try:
            return([
                self.sentence(command),
                self.is_user(user),
                self.is_blacklisted(command)
            ])
        except Exception as error:
            print(f"Error: self.encode({command}, {user}) -> {error}")

    def format_response_to_dataset(self, response) -> list:
        """Returns formatted response dataset from raw request"""
        try:
            out = []
            for action in response['users']:
                del action['id']
                del action['timestamp']
                found = re.search(r"(?<=\[Attempt\] Command:')(.*?)(?=')", action['comment'])
                if found is not None:
                    command = found.group()
                else:
                    command = ''
                out.append(self.encode(command, action['uid']))
            return(out)
        except Exception as error:
            print(f"Error: self.format_response_to_dataset([...]) -> {error}")

    def fromJSON(self, path='') -> dict:
        """Imports index from JSON file"""
        try:
            return(importJSON(path))
        except Exception as error:
            print(f"Error: self.fromJSON({path}) -> {error}")

    def toJSON(self, path='./exported_occurrences.json') -> None:
        """Exports current index to JSON file"""
        try:
            return(exportJSON(self.index, path))
        except Exception as error:
            print(f"Error: self.toJSON({path}) -> {error}")
#-----------------------------[ Predict model function ]---------------------------------#
def load_model(model_path, weights_path) -> tf.keras.models.Model:
    """Returns Keras model loaded from JSON file"""
    try:
        model = model_from_json(importJSON(model_path))
        model.load_weights(weights_path)
        model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )
        return(model)
    except Exception as error:
        print(f"Error: load_model({model_path}, {weights_path}) -> {error}")
#----------------------------[ Remove Duplicates function ]------------------------------#
def removeDuplicates(array) -> list:
    """Returns list with removed duplicates"""
    try:
        removed = []
        for i in array:
            if i in removed:
                removed.remove(i)
            else:
                removed.append(i)
        return(removed)
    except Exception as error:
        print(f"Error: removeDuplicates([...]) -> {error}")
#-------------------------------[ Create Folder function ]-------------------------------#
def createFolder(directory) -> None:
    """Returns None. Creates folder at specified directory if not exists"""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as error:
        print(f"Error: createFolder({directory}) -> {error}")
#-------------------------[ Split List by Percentage function ]--------------------------#
def split_by_percentage(data, percentage) -> tuple:
    """Returns tuple with a split list by percentage"""
    try:
        percentage = int(round(percentage*len(data)))
        return(data[percentage:], data[:percentage])
    except Exception as error:
        print(f"Error: split_by_percentage([...], {percentage}) -> {error}")
#--------------------------------[ Save model function ]---------------------------------#
def save_model(model, model_path) -> None:
    """Saves Keras model and weights to specified directory"""
    try:
        createFolder(model_path)
        exportJSON(model.to_json(), model_path+'/model.json')
        model.save_weights(model_path+'/model_weights.h5')
    except Exception as error:
        print(f"Error: save_model(model, {model_path}) -> {error}")
#-------------------------------[ OneHot Encoding class ]--------------------------------#
class OneHot:
    class Index:
        """Creates index object"""
        def __init__(self, vocabulary=list):
            self.vocabulary = removeDuplicates(vocabulary)
            self.table = self.create(vocabulary)

        def exists(self, string=str) -> bool:
            """Returns boolean value if string exists in table"""
            try:
                return(string in self.table)
            except Exception as error:
                print(f"Error: self.exists({string}) -> {error}")

        def add(self, string=str) -> bool:
            """Adds string to table if not exists"""
            try:
                if not self.exists(string):
                    self.table[string] = len(self.table)
                    return(True)
                else:
                    return(False)
            except Exception as error:
                print(f"Error: self.add({string}) -> {error}")

        def remove(self, string=str) -> None:
            """Removes string from table"""
            try:
                if self.exists(string):
                    del self.table[string]
            except Exception as error:
                print(f"Error: self.remove({string}) -> {error}")

        def create(self, vocabulary=list) -> dict:
            """Returns table from parameter list"""
            try:
                out = {}
                for i in range(len(vocabulary)):
                    out[vocabulary[i]] = i
                return(out)
            except Exception as error:
                print(f"Error: self.create([...]) -> {error}")
        
        def toJSON(self, file_path=str) -> None:
            """Saves current table to JSON file"""
            try:
                return(exportJSON([value[0] for value in self.table.items()], file_path))
            except Exception as error:
                print(f"Error: self.toJSON({file_path}) -> {error}")

    def __init__(self, vocabulary=list):
            self.vocabulary = vocabulary
            self.index = self.Index(vocabulary)

    def encode(self, word=str) -> int:
        """Returns encoded word value"""
        try:
            if not self.index.exists(word):
                self.index.add(word)
            return(self.index.table[word])
        except Exception as error:
                print(f"Error: self.encode({word}) -> {error}")

    def encode_sentence(self, sentence=str) -> list:
        """Returns encoded sentence to list of integer values"""
        try:
            sentence = sentence.split(' ')
            out = []
            for word in sentence:
                out.append(self.encode(word))
            return(out)
        except Exception as error:
                print(f"Error: self.encode_sentence({sentence}) -> {error}")

    def decode(self, number=int) -> str:
        """Returns decoded stirng from integer"""
        try:
            for key, value in self.index.table.items():
                if value == number:
                    return(key)
        except Exception as error:
                print(f"Error: self.decode({number}) -> {error}")

    def decode_sequence(self, sequence=list) -> str:
        """Returns decoded sentence from integer sequence list"""
        try:
            out = []
            for word in sequence:
                out.append(self.decode(word))
            return(out)
        except Exception as error:
                print(f"Error: self.decode_sequence({sequence}) -> {error}")

    def find(self, target):
        """Returns index key or value depending on parameter type"""
        try:
            if type(target) is int:
                for key, value in self.index.table.items():
                    if value == target:
                        return(key)
            elif type(target) is str:
                for key, value in self.index.table.items():
                    if key == target:
                        return(value)
        except Exception as error:
                print(f"Error: self.find({target}) -> {error}")

    def texts_to_sequences(self, targets=list) -> list:
        """Encodes a list of text to list of sequences"""
        try:
            out = []
            for target in targets:
                out.append(self.encode_sentence(target))
            return(out)
        except Exception as error:
                print(f"Error: self.texts_to_sequences([...]) -> {error}")