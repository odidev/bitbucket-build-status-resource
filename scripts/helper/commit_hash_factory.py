from .commit_hash_git import GitCommitHash
from .commit_hash_mercurial import MercurialCommitHash
import os


# Try and find out if it's a git or hg repo.
class CommitHashFactory:
    @classmethod
    def create(cls, artifact_directory):
        if os.path.exists(os.path.join(artifact_directory, '.hg')):
            return MercurialCommitHash(artifact_directory)
        elif os.path.exists(os.path.join(artifact_directory, '.git')):
            return GitCommitHash(artifact_directory)
        else:
            return None
