import praw
import prawcore
import yaml
import datetime
import os
import sys
import time

COMMENT_CONTENT = "There is a 180 character minimum for top level comments. This is to keep discussion in depth and prevent threads full of non in depth comments. If your comment doesn't meet the threshold, please post it as a reply to this comment."
CONFIG_PATH = os.getenv("RPN_CONFIG", "config.yml")
LOGGING = os.getenv("RPN_LOGGING", "FALSE")
YAML_KEY_CLIENT = "client"
YAML_KEY_SECRET = "secret"
YAML_KEY_AGENT = "agent"
YAML_KEY_PASSWORD = "password"
YAML_KEY_USERNAME = "username"

def main():
    print("Beginning bot")
    config = get_config()
    reddit = praw.Reddit(
        client_id=config[YAML_KEY_CLIENT],
        client_secret=config[YAML_KEY_SECRET],
        user_agent=config[YAML_KEY_AGENT],
        password=config[YAML_KEY_PASSWORD],
        username=config[YAML_KEY_USERNAME]
    )

    subreddit = reddit.subreddit("TrueFilm")
    while True:
        try:
            for submission in subreddit.stream.submissions(pause_after=None, skip_existing=True):
                print("subimtted", submission)
                submission.reply(COMMENT_CONTENT)
        except KeyboardInterrupt:
            sys.exit("\tStopping application, bye bye")

        except (praw.exceptions.PRAWException,
                prawcore.exceptions.PrawcoreException) as exception:
            print("Reddit API Error: ")
            print(exception)
            print("Pausing for 30 seconds...")
            time.sleep(30)
def get_config():
    """Returns application configuration."""
    check_config_file()
    return load_config()


def check_config_file():
    """Check if config file exists."""
    if not os.path.exists(CONFIG_PATH):
        sys.exit("Missing config file: " + CONFIG_PATH)

    print("Using config file: " + CONFIG_PATH)


def load_config():
    """Load config into memory."""
    with open(CONFIG_PATH, "r") as config_yaml:
        config = None

        try:
            config = yaml.safe_load(config_yaml)

        except yaml.YAMLError as exception:
            if hasattr(exception, "problem_mark"):
                mark = exception.problem_mark # pylint: disable=no-member
                print("Invalid yaml, line %s column %s" % (mark.line + 1, mark.column + 1))

            sys.exit("Invalid config: failed to parse yaml")

        if not config:
            sys.exit("Invalid config: empty file")

        return config

if __name__ == "__main__":
    main()
