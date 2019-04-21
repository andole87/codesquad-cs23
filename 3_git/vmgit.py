import os
import datetime
import json


class GitShell:
    command_dic = dict()
    git_json = dict()
    repos_list = []
    abspath_root_dir = os.path.dirname(os.path.abspath(__file__))
    current_repo_name = ""
    is_checkout = False

    def __init__(self, *args, **kwargs):
        self.command_dic = {
            "init": self.init_git, "status": self.status_git,
            "checkout": self.checkout_git, "new": self.new_git,
            "add": self.add_git, "commit": self.commit_git,
            "log": self.log_git
        }

        self.repos_list = [name for name in os.listdir(self.abspath_root_dir)
                           if os.path.isdir(os.path.join(self.abspath_root_dir, name))]

        self.git_json = {
            "working_tree": {
                "untracked": {},
                "unmodified": {},
                "modified": {},
            },
            "staged": {},
            "git_repo": {},
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

        if _parsed_command[0] == "status":
            self.status_git()
        elif _parsed_command[0] == "log":
            self.log_git()
        else:
            self.command_dic[_parsed_command[0]](_parsed_command[1])

    def init_git(self, repo_name):
        if repo_name == "":
            raise Exception('You must give me repository name')
        repo_path = os.path.join(self.abspath_root_dir, repo_name)
        os.makedirs(repo_path)
        with open(os.path.join(repo_path, 'git.json'), 'w') as f:
            json.dump(self.git_json, f)
        self.repos_list.append(repo_name)
        print("created  <{}> repository.".format(repo_name))

    def status_git(self):
        if self.is_checkout:
            self.checkout_status()
        else:
            print("\n".join(self.repos_list))

    def checkout_status(self):
        print(self.git_json["working_tree"])

    def checkout_git(self, repo_name):
        if not repo_name in self.repos_list:
            raise Exception("{} not exsits".format(repo_name))

        if self.is_checkout:
            with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'w') as f:
                f.write(json.dumps(self.git_json, indent=2))

        print("/{}/checkout".format(repo_name))
        self.is_checkout = True
        self.current_repo_name = repo_name
        with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'r') as f:
            self.git_json = json.load(f)

    def new_git(self, file_name):
        f = open(os.path.join(self.abspath_root_dir,
                              self.current_repo_name, file_name), 'w+')
        f.close()
        self.git_json["working_tree"]["untracked"][file_name] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'w') as f:
            f.write(json.dumps(self.git_json, indent=2))

    def add_git(self, file_name):
        if file_name == ".":
            target = self.git_json["working_tree"]["untracked"] + self.git_json["working_tree"]["modified"]
        else:
            if file_name in self.git_json["working_tree"]["untracked"].keys():
                target = {file_name: self.git_json["working_tree"]["untracked"][file_name]}
            elif file_name in self.git_json["working_tree"]["modified"].keys():
                target = {file_name: self.git_json["working_tree"]["untracked"][file_name]}

        for x in target.keys():
            self.git_json["staged"][x] = target[x]

        with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'w') as f:
            f.write(json.dumps(self.git_json, indent=2))

    def commit_git(self, commit_log):
        target = self.git_json["staged"]
        print(target)
        self.git_json["git_repo"][commit_log] = target

        self.git_json["staged"] = {}

        with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'w') as f:
            f.write(json.dumps(self.git_json, indent=2))

    def log_git(self):
        print(self.git_json["git_repo"])


if __name__ == "__main__":
    git = GitShell()
    git.git_shell_run()
