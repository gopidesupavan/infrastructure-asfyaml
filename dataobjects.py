import pathlib
import mappings


class Repository:
    """Simple class that holds information about the repository (and branch) being processed.

    :parameter path: The filesystem path to the .git directory for this repository.

    Example::

        import dataobjects
        repo = dataobjects.Repository("/x1/repos/asf/tomcat/tomcat9.git")
        assert repo.is_private is False, "This should not be a private repo!"
        website = f"https://{repo.hostname}.apache.org/"

    """
    def __init__(self, path):
        #: str|Pathlike: The filesystem path to this repository directory
        self.path = pathlib.Path(path)
        #: str: The name of this repository (sans the .git part), for instance :samp:`whimsy-website`.
        self.name = self.path.name.removesuffix(".git")

    @property
    def is_private(self):
        """"Set to True if the repository is a private repository, False if it is public"""
        return "private" in self.path.parts

    @property
    def project(self):
        """Returns the LDAP name of the project owning this repository, for instance httpd or openoffice"""
        match = mappings.REPO_RE.match(self.name)
        if match:
            return match.group(1)
        return "infrastructure"   # Weird repo name, default to infra owning it.

    @property
    def hostname(self):
        """Returns the hostname for the project. httpd for httpd, but whimsical for whimsy."""
        return mappings.LDAP_TO_HOSTNAME.get(self.project, self.project)


class Committer:
    """"Simple info class for committer(pusher) of code"""
    def __init__(self, username):
        #: str: The ASF user id of the person that pushed this commit, for instance :samp:`humbedooh`
        self.username = username
        #: str: The ASF email address of the person that pushed this commit, for instance :samp:`humbedooh@apache.org`.
        self.email = f"{username}@apache.org"
