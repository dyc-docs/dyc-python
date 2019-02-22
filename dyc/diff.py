"""
Ideally, this file is to get the current staged
in Git Diff, then creates a `.dyc.patch` temporary file.

The file will patch will undergo the process of:
1 - See where the `Added` lines fall in
2 - Extract methods that fall within the added lines and dump them into `.dyc.patch`
"""
import os
import git
import ntpath

class DiffParser(object):

    PREFIX = 'diff --git'

    def parse(self, staged=False):
        # self.plain_diff = self.repo.git.diff('HEAD')
        self.diffs = self.repo.index.diff('HEAD' if staged else None)
        self.plain = self.repo.git.diff('HEAD').split('\n')
        return self._pack()

    def _pack(self):
        patches = []
        for diff in self.diffs:
            sep = '{} a/{} b/{}'.format(self.PREFIX, diff.a_path, diff.b_path)
            patch = self.__clean(self.__patch(sep), diff)
            patches.append(patch)
        return patches

    def __patch(self, separator):
        patch = []
        hit = False
        # end = False
        for line in self.plain:
            if line == separator:
                hit = True
                continue
            elif line.startswith(self.PREFIX) and hit:
                break
            elif hit:
                patch.append(line)
        return '\n'.join(patch)

    def __clean(self, patch, diff):
        """Returns a clean dict of a path"""

        result = {}
        result['additions'] = self.__additions(patch)
        result['hunk'] = self.__hunk(patch)
        result['plain'] = patch
        result['diff'] = diff
        result['name'] = ntpath.basename(diff.a_path)
        result['path'] = diff.a_path
        return result

    def __hunk(self, patch):
        import re
        pat = r'.*?\@\@(.*)\@\@.*'
        match = re.findall(pat, patch)
        return [m.strip() for m in match]

    def __additions(self, patch):
        dumps = []
        s = patch.split('\n')
        for line in s:
            try:
                if line[0] == '+' and not line.startswith('+++'):
                    l = line[1:]
                    dumps.append(l)
            except IndexError:
                continue
        return '\n'.join(dumps)


class Diff(DiffParser):
    def __init__(self):
        self.repo = git.Repo(os.getcwd())

    @property
    def uncommitted(self):
        return self._uncommitted()

    def _uncommitted(self):
        return self.parse()
