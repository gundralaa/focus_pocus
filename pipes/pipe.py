# Generic Pipe Class
# fn: apply fn, out: opt log fn, name: opt str
class Pipe:
    def __init__(self, fn, out=None, name=''):
        self.fn = fn
        self.out = out
        self.name = name or 'none'

    # return val or (arr)
    # SPECIFY IN and OUT in pipe descr
    def apply(self, data):
        val = self.fn(data)
        if self.out: self.out(val)
        return val
    
    def __repr__(self) -> str:
        desc = 'name: ' + self.name
        return desc