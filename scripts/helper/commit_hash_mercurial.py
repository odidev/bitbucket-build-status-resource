from helper import CommitHash
import subprocess


class MercurialCommitHash(CommitHash):
    def __str__(self):
        return subprocess.check_output(
            ['hg', '-R', self.directory, 'log', '--rev', '.', '--template', '{node}']
        ).strip().decode()
