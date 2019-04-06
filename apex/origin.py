import json
import re

from bs4 import BeautifulSoup

from apex.util import GET, POST, GenerateCID

fidURL = "https://accounts.ea.com/connect/auth?response_type=code&client_id=ORIGIN_SPA_ID&display=originXWeb/login&locale=en_US&release_type=prod&redirect_uri=https://www.origin.com/views/login.html"
loginURL = "https://accounts.ea.com/connect/auth?client_id=ORIGIN_JS_SDK&response_type=token&redirect_uri=nucleus:rest&prompt=none&release_type=prod"
logoutURL = "https://accounts.ea.com/connect/logout?client_id=ORIGIN_JS_SDK&access_token={}&redirect_uri=nucleus:rest"


class Origin:
    """ToDo"""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def Login(self):
        """Login to Origin using the client's credentials."""

        location = self.GetFID()
        location = self.GetJSessionID(location)
        self.GetAuthPage(location)
        location = self.AuthorizeLogin(location)
        location = self.GetSID(location)
        self.GetAccessToken()
        self.GetInternalUser()

    def Logout(self):
        """Logout of the current Origin session."""

        try:
            url = logoutURL.format(self.accessToken)
            res = GET(url)

            # HTTP 200 (OK).
            if res.status_code == 200:
                return True
            else:
                return False
        except AttributeError:
            # accessToken not present, not logged-in.
            pass

    def GetFID(self):
        """Return the FID required for login."""

        res = GET(fidURL)

        # HTTP 302 (Redirect).
        if res.status_code == 302:
            self.fid = re.search(
                "(?<=fid=)[a-zA-Z0-9]+?(?=&|$)", res.headers["Location"]
            ).group(0)

            return res.headers["Location"]

    def GetJSessionID(self, location: str):
        """Return the JSessionID required for login."""

        res = GET(location)

        # HTTP 302 (Redirect).
        if res.status_code == 302:
            self.jSessionID = re.search(
                r"(?<=JSESSIONID=)[\S]+?(?=;)", res.headers["Set-Cookie"]
            ).group(0)

            return f"https://signin.ea.com{res.headers['Location']}"

    def GetAuthPage(self, location: str):
        """Return the Authorization Page location required for login."""

        headers = {"Cookie": f"JSESSIONID={self.jSessionID}"}
        res = GET(location, headers=headers)

        # HTTP 302 (Redirect).
        if res.status_code == 302:
            self.jsession = re.search(
                r"(?<=JSESSIONID=)[\S]+?(?=;)", res.headers["Set-Cookie"]
            ).group(0)

            return res.headers["Location"]

    def AuthorizeLogin(self, location: str):
        """ToDO"""

        headers = {"Cookie": f"JSESSIONID={self.jSessionID}"}
        data = {
            "email": self.email,
            "password": self.password,
            "_eventId": "submit",
            "cid": GenerateCID(32),
            "showAgeUp": "true",
            "googleCaptchaResponse": "",
            "_rememberMe": "on",
        }
        res = POST(location, headers=headers, data=data)

        # HTTP 200 (OK).
        if res.status_code == 200:
            return re.search(r'(?<=window\.location = ")\S+(?=";)', res.text).group(0)

    def GetSID(self, location: str):
        """Return the SID required for login."""

        res = GET(location)

        # HTTP 302 (Redirect).
        if res.status_code == 302:
            self.sid = re.search(
                r"(?<=sid=)[\S]+?(?=;)", res.headers["Set-Cookie"]
            ).group(0)

            self.code = re.search(
                r"(?<=code=)[\S]+?(?=&|$)", res.headers["Location"]
            ).group(0)

        return res.headers["Location"]

    def GetAccessToken(self):
        """Return the Access Token required for login."""

        headers = {"Cookie": f"sid={self.sid}"}
        res = GET(loginURL, headers=headers)

        # HTTP 200 (OK).
        if res.status_code == 200:
            res = json.loads(res.text)
            self.accessToken = res["access_token"]

    def GetInternalUser(self):
        """Return the current userID."""

        headers = {"Authorization": f"Bearer {self.accessToken}"}
        url = "https://gateway.ea.com/proxy/identity/pids/me"
        res = GET(url, headers=headers)
        res = json.loads(res.text)
        self.userID = res["pid"]["pidId"]

    def SearchUser(self, username: str, platform: str):
        """
        Search for an Origin, PlayStation 4, or Xbox One player given
        the specified username.

        Valid platforms: `PC`, `PS4`, `XB1`
        """

        if platform.lower() == "pc":
            return self.SearchPCUser(username)
        if platform.lower() == "ps4":
            return "PlayStation 4 platform support not implemented"
        if platform.lower() == "xb1":
            return "Xbox One platform support not implemented"
        else:
            return "Invalid platform specified"

    def SearchPCUser(self, username: str):
        """ToDo"""

        headers = {"authtoken": self.accessToken}
        url = f"https://api1.origin.com/xsearch/users?userId={self.userID}&searchTerm={username}&start=0"
        res = GET(url, headers=headers)

        # HTTP 200 (OK).
        if res.status_code == 200:
            res = json.loads(res.text)

            results = []

            # Only allowed up to lookup 5 userIDs, limit results to 5.
            if res["infoList"] is not None:
                for result in res["infoList"][:5]:
                    userID = result["friendUserId"]
                    results.append(userID)

                parameter = ",".join(results)
                headers = {"authtoken": self.accessToken}
                url = f"https://api1.origin.com/atom/users?userIds={parameter}"
                res = GET(url, headers=headers)

                # HTTP 200 (OK).
                if res.status_code == 200:
                    res = BeautifulSoup(res.text, "xml")

                    for result in res.users:
                        if result.EAID.string.lower() == username.lower():
                            return result.userId.string, result.EAID.string
            else:
                return "No results"
