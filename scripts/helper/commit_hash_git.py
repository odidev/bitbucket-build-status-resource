from helper import CommitHash
import subprocess


class GitCommitHash(CommitHash):
    def __str__(self):
        return subprocess.check_output(
            ['git', '-C', self.directory, 'rev-parse', 'HEAD']
        ).strip().decode()
