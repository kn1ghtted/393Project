import collections
class MyOrderedDict(collections.OrderedDict):
  def next_key(self, key):
    next = self._OrderedDict__map[key][1]
    if next is self._OrderedDict__root:
      raise ValueError("{!r} is the last key".format(key))
    return next[2]
  
  def first_key(self):
    for key in self: return key
    raise ValueError("OrderedDict() is empty")