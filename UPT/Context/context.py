import sys
import os

class DDict(object):
    def __init__(self, init_dict = None):
        self.back = {}
        self.front = {}

    def __getitem__(self,item):
        return (self.front[item])

    def __setitem__(self,item,val):
        self.front[item] = val
        self.back[val] = item

    def __contains__(self, item):
        try:
            self.front[item]
        except KeyError:
            return False
        return True

    def get_front(self):
        return self.front

    def get_back(self):
        return self.back

    def __hash__(self):
        return hash(self.back) + hash(self.front)


class ContextManager(object):
    def __init__(self):
        self.unique_words = 0
        self.total_contexts = 0
        self.contexts = {}
        super().__init__()

    def __getitem__(self, item):
        if item not in self.contexts:
            c = Context(item)
            self.contexts[item] = c
        return self.contexts[item]

    def add_w_context(self, word, context):
        self.contexts[word] = context

    def add_context(self, context, pre, post):
        if pre in self.contexts:
            pre = self.contexts[pre]
        else:
            pr = Context(pre)
            self.add_w_context(pre, pr)
            pre = pr

        if post and post in self.contexts:
            post = self.contexts[post]
        else:
            if post:
                po = Context(post)
                self.add_w_context(post, po)
                post = po
        context.add_context(pre, post)


class Context(object):
    def __init__(self, token, obj=DDict()):
        self.token = token
        self.__context = obj
        super().__init__()

    def __hash__(self):
        return hash(self.token)

    def get_context(self):
        return (self.__context.get_front(), self.__context.get_back())

    def add_context(self, contexta, contextb):
        if contexta and contexta not in self.__context:
            self.__context[contexta] = 1
        elif contexta:
            self.__context[contexta] += 1

        if contextb and contextb not in self.__context:
            self.__context[contextb] = 1
        elif contextb:
            self.__context[contextb] += 1
