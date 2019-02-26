import argparse, json, os, sys

DEFAULT_USER = "chris-hamberg"

def make(repo, user):
    url = "https://api.github.com/user/repos"
    data = json.dumps({"name": repo})
    command = f"curl -u '{user}' {url} -d '{data}'"
    print(command)
    #os.system(command)

def parse(args):
    parser = argparse.ArgumentParser(
            description="Create a new Github repository on Github.com.")
    parser.add_argument("-r", "--repo", help="Github repo name.", required=True)
    parser.add_argument("-u", "--user", help="Github username.")
    parsed = parser.parse_args(args)

    return parsed

def main():
    args = parse(sys.argv[1:])
    user = DEFAULT_USER if args.user != '' else args.user
    make(args.repo, user)

if __name__ == "__main__":
    main()
