class Buf:
    """
    Maintain the following:
    - a "sliding window" of characters read from the buffer
    - a histogram of the characters currently in the window
    - a "uniqueness" condition which will be TRUE if all characters in the buffer are different from each other
    - a count of characters read up to the most recent one
    """
    def __init__(self, buf_str, window_size):
        self.buf_str = buf_str                              # the entire buffer string
        self.window_size = window_size                      # the length of the sliding window
        self.read_idx = 3                                   # the index of the most recently read character in the buffer string
        self.last_char_idx = len(buf_str) - 1               # the index of the last character in the buffer string
        self.window = list(buf_str[0:window_size])          # a sliding window of the {window_size} most recently read characters
        self.hist = dict()                                  # a histogram view of the sliding window
        for i in self.window:
            if i not in self.hist:
                self.hist[i] = 1
            else:
                self.hist[i] += 1

    def next(self) -> bool:
        """
        Sliding window moves to the right, and we update the histogram to reflect the current state of the window.
        Return False if we've hit the end of the buffer string, else True.

        Invariants:
        - len(window) == window_size
        - len(hist) <= window_size
        - sum(hist.values() == window_size)
        - read_count <= len(buf_str)
        """
        if self.read_idx >= self.last_char_idx:
            return False

        self.read_idx += 1

        # move sliding window to the right by adding a new character to the right side of the list and ejecting the left-most
        next_char = self.buf_str[self.read_idx]
        self.window.append(next_char)
        ejected_char = self.window.pop(0)

        # add an occurence of the new character to the histogram
        if next_char not in self.hist:
                self.hist[next_char] = 1
        else:
            self.hist[next_char] += 1

        # remove an occurrence of the ejected character from the histogram
        self.hist[ejected_char] -= 1
        if self.hist[ejected_char] == 0:
            self.hist.pop(ejected_char)

        return True

    def isPacketStartFound(self) -> bool:
        return len(self.hist) == self.window_size

    def getPacketStart(self) -> int:
        return self.read_idx + 1

def parts1and2():
    buf = None
    with open("6_input.txt", "r") as f:
        # buf = Buf(f.readline(), 4) # part 1
        buf = Buf(f.readline(), 14) # part 2
    if buf is not None:
        while not buf.isPacketStartFound() and buf.next():
                continue
        if buf.isPacketStartFound():
            print(buf.getPacketStart())
        else:
            print("Packet start not found.")

parts1and2()