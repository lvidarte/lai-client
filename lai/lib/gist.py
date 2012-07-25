from github import Github, InputFileContent

class GistException(Exception):
    pass

class Gist:

    def __init__(self, username, password):
        self._g = Github(username, password)

    def create(self, public, doc):
        try:
            user = self._g.get_user()
            file_name = "%s.sh" % doc.id
            created_gist = user.create_gist(public, {file_name: InputFileContent(doc.data)}, 'created from lai')
            return created_gist.html_url
        except Exception as e:
            raise GistException(e)


