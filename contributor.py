import json
from util import write_to_json 
import sys

from util import make_request


class Contributor:
    def __init__(self, type, contributions=0):
        """
        Parameters:
        type: type of contributor (User, Anonymous)
        """
        self.type = type
        self.contributions = contributions
        self.commits = None


class UserContributor(Contributor):
    def __init__(self, login, id, url, repos_url, 
        site_admin, contributions=0):
        """
        Parameters:
        login: login of the contributor
        id: id of the contributor
        url: github url of the contributor
        repos_url: github url of contributor's repositories
        site_admin: true if the contributor is an admin
        contributions: number of contributions (commits) in the repo
        """

        super().__init__("User", contributions)
        self.login = login
        self.id = id 
        self.url = url
        self.repos_url = repos_url
        self.site_admin = site_admin 


class AnonymousContributor(Contributor):
    def __init__(self, email, name, contributions=0):
        super().__init__("Anonymous", contributions)
        self.email = email
        self.name = name 


def get_contributor_from_dict(contributor):
    """
    Paramaters:
    contributor: dictionary 

    Returns: object UserContributor or AnonymousContributor
    """

    if contributor:
        if contributor["type"] == "User" or contributor["type"] == "Bot":
            login = contributor["login"]
            id = contributor["id"] 
            url = contributor["url"]
            repos_url = contributor["repos_url"]
            site_admin = contributor["site_admin"]
            return UserContributor(login, id, url, repos_url, 
                site_admin)
        elif contributor["type"] == "Anonymous":
            email = contributor["email"]
            name = contributor["name"]
            return AnonymousContributor(email, name)
        else: 
            print("OTHER TYPE")
    else: 
        pass


def get_contributors(token):
    """
    Returns:
    list of Contributor objects
    """

    i = 1
    contributors_list = []

    while True:
        params = {
            "per_page": "100",
            "page": str(i),
            "anon": "1"
        }
        url = "https://api.github.com/repos/facebook/react/contributors"
        contributors = make_request(url, token, params=params)
        
        print("REQUEST FOR " + str(i) + " PAGE OK")

        if not contributors:
            break

        i += 1

        for contributor in contributors:
            print(contributor)
            if contributor["type"] == "User" or contributor["type"] == "Bot":
                login = contributor["login"]
                id = contributor["id"]
                url = contributor["url"]
                repos_url = contributor["repos_url"]
                site_admin = contributor["site_admin"]
                contributions = contributor["contributions"]
                contributor_obj = UserContributor(
                    login, id, url, repos_url, site_admin, contributions
                )
            elif contributor["type"] == "Anonymous":
                email = contributor["email"]
                name = contributor["name"]
                contributions = contributor["contributions"]
                contributor_obj = AnonymousContributor(
                    email, name, contributions
                )
                
            
            contributors_list.append(contributor_obj)

    return contributors_list


def read_json_contributors():
    with open("contributors.json") as f:
        contributors = json.load(f)

    return contributors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give an authentification token from github api")
        exit(1)
    
    token = sys.argv[1]

    contributors = get_contributors(token)
    write_to_json("contributors.json", contributors)