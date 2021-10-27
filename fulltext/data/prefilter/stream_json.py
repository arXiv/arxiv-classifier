# File: stream_json.py
# Desc: Given an open json file, that has a top level array,
#       return 1 array item at a time.
#       No validation.

class StreamJson:
 
  IN_ARRAY    = 1                      # The top level array
  IN_QUOTES   = 2                      # Strings can have: ,[]{}
  AT_COMMA    = 3                      # Between top level items
  ARRAY_END   = 4

  def __init__(self, read):
    self.read      = read
    self.state     = None
    self.num_items = -1                # Stop after items reached

  def __iter__(self):
    return self

  def __next__(self):
    return self.next()

  def next(self):
    if self.state == self.ARRAY_END or self.num_items == 0:
      raise StopIteration()
    self.num_items -= 1

    if not self.state:
      c = self.read.read(1)
      while c and c != '[':            # Read to start of json array
        c = self.read.read(1)
      if c == '[':
        self.state = self.IN_ARRAY

    if self.state == self.AT_COMMA:    # Begin next item
      self.state = self.IN_ARRAY

    buf   = ''
    depth = 0
    c = self.read.read(1)
    while c and self.state not in [self.AT_COMMA, self.ARRAY_END]:
      #print(f'1.  S={self.state}  D={depth}  c={c}  buf={buf[:40]}...')
                                       # End of array
      if self.state == self.IN_ARRAY and depth == 0 and c == ']':
        self.state = self.ARRAY_END
                                       # End of item
      elif self.state == self.IN_ARRAY and depth == 0 and c == ',':
        self.state = self.AT_COMMA
                                       # Start of quoted string
      elif self.state == self.IN_ARRAY and c == '"':
        self.state = self.IN_QUOTES
        buf   += c
        c = self.read.read(1)
                                       # Handle string text
      elif self.state == self.IN_QUOTES:
        if c == '\\':
          buf   += c
          c = self.read.read(1)        # Read the escaped char
          buf   += c
        elif c == '"':                 # End of quoted string
          self.state = self.IN_ARRAY
          buf   += c
        else:                          # Store everything else
          buf   += c
        c = self.read.read(1)

      else:                            # Track nested objects
        if c in ['{', '[']:
          depth += 1
        elif c in ['}', ']']:
          depth -= 1
                                       # Store everything
        buf   += c
        c = self.read.read(1)

    return buf

if __name__ == '__main__':
  import sys
  if len(sys.argv) >= 2:
    file_name = sys.argv[1]
  else:
    file_name = 'test/7.json'

  print()
  print(f'============================ CAT {file_name} ==')
  with open(file_name) as f:
    print(f.read())

  print(f'============================ START JSON ITEMS ==========')
  with open(file_name) as f:
    sj = StreamJson(f)
    for item in sj:
      print(f'item:{item}')

