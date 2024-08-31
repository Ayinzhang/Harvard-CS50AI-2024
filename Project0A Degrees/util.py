class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, path: list):
        self.frontier.append(path)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self) -> list:
        if self.Empty():
            raise Exception("empty frontier")
        else:
            path = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return path


class QueueFrontier(StackFrontier):

    def remove(self) -> list:
        if self.Empty():
            raise Exception("empty frontier")
        else:
            path = self.frontier[0]
            self.frontier = self.frontier[1:]
            return path
