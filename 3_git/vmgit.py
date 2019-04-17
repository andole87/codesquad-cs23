import os
import datetime
import time
import json


class GitShell:
    command_dic = dict()
    repos_list = []
    abspath_root_dir = os.path.dirname(os.path.abspath(__file__))
    current_repo_name = ""
    is_checkout = False
    git_json = dict()

    def __init__(self, *args, **kwargs):
        self.command_dic = {
            "init": self.init_git, "status": self.status_git,
            "checkout": self.checkout_git, "new": self.new_git,
            "add": self.add_git, "commit": self.commit_git,
            "log": self.log_git}
        self.repos_list = [name for name in os.listdir(self.abspath_root_dir)
                           if os.path.isdir(os.path.join(self.abspath_root_dir, name))]
        self.git_json = {
            "untracked": ["--Working Directory--"],
            "unmodified": ["--Unmodified--"],
            "modified": ["--Modified--"],
            "staged": ["--Staging Area--"],
            "git_repo": ["--Git Repository--"],
            "log": ["--Commit Log--"]
        }

    def git_shell_run(self):
        try:
            while True:
                input_command = input(
                    "andole_vmgit_prompt {}>>".format(self.current_repo_name))
                if input_command == "exit":
                    break
                self.parse_command(input_command)
        except Exception as err:
            print(err)
            self.git_shell_run()

    def parse_command(self, input_command):
        _parsed_command = input_command.split()
        try:
            if _parsed_command[0] == "status":
                self.status_git()
            elif _parsed_command[0] == "log":
                self.log_git()
            else:
                self.command_dic[_parsed_command[0]](_parsed_command[1])
        except Exception as err:
            raise err

    def init_git(self, repo_name):
        if repo_name == "":
            raise Exception('You must give me repository name')
        repo_path = os.path.join(self.abspath_root_dir, repo_name)
        os.makedirs(repo_path)
        with open(os.path.join(repo_path, 'git.json'), 'w') as f:
            json.dump(self.git_json, f)
        self.repos_list.append(repo_name)
        print("created  [{}] repository.".format(repo_name))

    def status_git(self):
        if self.is_checkout:
            self.checkout_status()
        else:
            print("\n".join(self.repos_list))

    def checkout_status(self):
        print(self.git_json)

    def checkout_git(self, repo_name):
        if not repo_name in self.repos_list:
            raise Exception("{} not exsits".format(repo_name))

        if self.is_checkout:
            with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'w') as f:
                json.dump(self.git_json, f)

        print("/{}/checkout".format(repo_name))
        self.is_checkout = True
        self.current_repo_name = repo_name
        with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'r') as f:
            self.git_json = json.load(f)

    def new_git(self, file_name):
        open(os.path.join(self.abspath_root_dir,
                          self.current_repo_name, file_name), 'w')
        self.git_json["untracked"].append("{} {}"
                                          .format(file_name, datetime.datetime
                                                  .strptime(time.ctime(os.path.getmtime(file_name)), "%Y-%m-%d %H:%M:%S")))

    def add_git(self, file_name):
        target = self.git_json["untracked"][1:] + self.git_json["modified"][1:]
        self.git_json["staged"] += target

        self.git_json["untracked"] = [x for x in self.git_json["untracked"] if not x in target]
        self.git_json["modified"] = [x for x in self.git_json["modified"] if not x in target]

    def commit_git(self, commit_log):
        target = self.git_json["staged"][:1]
        print("Commited these file..\n" + target)
        self.git_json["git_repo"] += target
        self.git_json["log"]


        self.git_json["staged"] = self.git_json["staged"][:1]




    def log_git(self):
        pass


if __name__ == "__main__":
    git = GitShell()
    git.git_shell_run()
