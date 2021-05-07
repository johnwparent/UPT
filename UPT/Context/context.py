import sys
import os


class DDict(object):
    def __init__(self, init_dict = None):
        self.back = {}
        self.front = {}

    def __getitem__(self,item):
        return (self.front[item],self.back[self.front[item]])

    def __setitem__(self,item,val):
        self.front[item] = val
        self.back[val] = item

    def __hash__(self):
        return hash(self.back) + hash(self.front)


class ContextManager(object):
    def __init__(self):
        self.unique_words = 0
        self.total_contexts = 0
        self.contexts = set()
        super().__init__()


    def add_context(self, context):
        pass

class Context(object):
    def __init__(self, token, obj=DDict()):
        self.token = token
        self.__context = obj
        super().__init__()

    def __hash__(self):
        return int(self.token)

    def add_context(self, context):
        self.__context[context]





