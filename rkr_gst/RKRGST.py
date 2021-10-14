from .RollingAdler import RollingAdler
from .Match import Match
from typing import List

class RKRGST(object):
    def __init__(self, pattern: str, text: str) -> None:
        self.__pattern = pattern
        self.__text = text
        self.__pattern_length = len(pattern)
        self.__pattern_mark = [0] * self.__pattern_length
        self.__text_length = len(text)
        self.__text_mark = [0] * self.__text_length
        self.matches: List[Match] = []
        self.result: List[Match] = []

    @property
    def text(self) -> str:
        return self.__text

    @property
    def pattern(self) -> str:
        return self.__pattern

    @staticmethod
    def run(p: str, t: str, search_length: int, minimum_match_length: int) -> List[Match]:
        s = search_length
        params = RKRGST(p, t)
        while True:
            lmax = params.scan_pattern(s)
            if lmax > 2 * s:
                s = lmax
            else:
                params.mark_strings()
                if s > 2 * minimum_match_length:
                    s //= 2
                elif s > minimum_match_length:
                    s = minimum_match_length
                else:
                    break

        return params.result

    def scan_pattern(self, search_length: int) -> int:
        map = { }
        i = 0
        while (i + search_length) <= self.__text_length:
            for j in range(i, i + search_length):
                if self.__text_mark[j]:
                    i = j + 1
                    break
            if i + search_length > self.__text_length:
                break

            hash = RollingAdler.new()
            for j in range(i, i + search_length):
                hash.update(ord(self.__text[j]))

            while True:
                if self.__text_mark[i + search_length - 1]:
                    break

                if map.get(hash.hash()) is None:
                    map[hash.hash()] = [i]
                else:
                    map[hash.hash()].append(i)
                i = i + 1
                if i + search_length > self.__text_length:
                    break

                hash.remove(search_length, ord(self.__text[i - 1]))
                hash.update(ord(self.__text[i + search_length - 1]))

        self.matches.clear()
        i = 0
        max_match = 0
        while (i + search_length) <= self.__pattern_length:
            for j in range(i, i + search_length):
                if self.__pattern_mark[j]:
                    i = j + 1
                    break
            if i + search_length > self.__pattern_length:
                break

            hash = RollingAdler.new()
            for j in range(i, i + search_length):
                hash.update(ord(self.__pattern[j]))

            while True:
                if self.__pattern_mark[i + search_length - 1]:
                    break
                if map.get(hash.hash()):
                    for text_idx in map[hash.hash()]:
                        pattern_index = i
                        k = 0
                        while text_idx + k < self.__text_length and\
                            pattern_index + k < self.__pattern_length and\
                            self.__text[text_idx + k] == self.__pattern[pattern_index + k] and\
                            not self.__text_mark[text_idx + k] and\
                            not self.__pattern_mark[pattern_index + k]:
                            k = k + 1
                            if k > 2 * search_length:
                                return k
                            if k >= search_length:
                                self.matches.append(Match(pattern_index=pattern_index, text_index=text_idx, length=k))
                                max_match = max(max_match, k)
                i += 1
                if i + search_length > self.__pattern_length:
                    break
                hash.remove(search_length, ord(self.__pattern[i - 1]))
                hash.update(ord(self.__pattern[i + search_length - 1]))
        return max_match
    
    def mark_strings(self) -> None:
        for m in self.matches:
            unmarked = True
            for i in range(m.length):
                if self.__text_mark[m.text_index + i] or self.__pattern_mark[m.pattern_index + i]:
                    unmarked = False
                    break
            if unmarked:
                self.result.append(m)
                for i in range(m.length):
                    self.__text_mark.insert(m.text_index + i, 1)
                    self.__pattern_mark.insert(m.pattern_index + i, 1)
        self.matches.clear()


if __name__ == '__main__':
    print(RKRGST.run('lower', 'yellow', 3, 2))