import os
import datetime
import json


class GitShell:
    command_dic = dict()
    git_json = dict()
    repos_list = []
    abspath_root_dir = os.path.dirname(os.path.abspath(__file__))
    current_repo_name = ""

    def __init__(self, *args, **kwargs):
        self.command_dic = {
            "init": self.init_git, "status": self.status_git,
            "checkout": self.checkout_git, "new": self.new_git,
            "add": self.add_git, "commit": self.commit_git,
            "log": self.log_git,
            "touch": self.touch_git,
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
        if self.current_repo_name == "":
            print("\n".join(self.repos_list))
        else:
            self.checkout_status()

    def checkout_status(self):
        print(self.git_json["working_tree"])

    def checkout_git(self, repo_name):
        if not repo_name in self.repos_list:
            raise Exception("{} not exsits".format(repo_name))

        print("/{}/checkout".format(repo_name))
        self.current_repo_name = repo_name
        self.load_json()

    def new_git(self, file_name):
        f = open(os.path.join(self.abspath_root_dir,
                              self.current_repo_name, file_name), 'w+')
        f.close()
        self.git_json["working_tree"]["untracked"][file_name] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        self.save_json()

    def add_git(self, file_name):

        if file_name in self.git_json["working_tree"]["untracked"]:
            target_info = self.git_json["working_tree"]["untracked"].pop(file_name)
        elif file_name in self.git_json["working_tree"]["modified"]:
            target_info = self.git_json["working_tree"]["modified"].pop(file_name)
        else:
            raise Exception("{} not exist.".format(file_name))

        self.git_json["staged"][file_name] = target_info
        self.save_json()

    def commit_git(self, commit_log):
        target = self.git_json["staged"]
        for f in target:
            self.git_json["working_tree"]["unmodified"][f] = target[f]

        self.git_json["git_repo"][commit_log] = target
        self.git_json["staged"] = {}

        self.save_json()

    def touch_git(self, file_name):

        for commit_message in self.git_json["git_repo"]:
            if file_name in self.git_json["git_repo"][commit_message]:
                self.git_json["working_tree"]["unmodified"].pop(file_name)
                self.git_json["working_tree"]["modified"][file_name] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_json()
                return
        
        self.new_git(file_name)

    def save_json(self):
        with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'w') as f:
            f.write(json.dumps(self.git_json, indent=2))

    def load_json(self):
        with open(os.path.join(self.abspath_root_dir, self.current_repo_name, 'git.json'), 'r') as f:
                f.write(json.dumps(self.git_json, indent=2))

    def log_git(self):
        print(self.git_json["git_repo"])


if __name__ == "__main__":
    git = GitShell()
    git.git_shell_run()