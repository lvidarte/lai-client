# -*- coding: utf-8 -*-

# Author: Leo Vidarte <http://nerdlabs.com.ar>
#
# This file is part of lai-client.
#
# lai-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# lai-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lai-client. If not, see <http://www.gnu.org/licenses/>.

from github import Github, InputFileContent

class Gist:

    def __init__(self, username, password):
        self._g = Github(username, password)

    def create(self, public, doc):
        user = self._g.get_user()
        file_name = "lai-%s" % doc.id
        content = {file_name: InputFileContent(doc.data.content)}
        description = '' if doc.data.description is None else doc.data.description
        created_gist = user.create_gist(public, content, description)
        return created_gist.html_url


