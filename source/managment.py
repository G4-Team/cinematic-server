import argparse
import os
import subprocess

from settings.base import APPS, BASE_DIR


class ManagementUtility:

    @classmethod
    def createparser(cls):
        parser = argparse.ArgumentParser(description="manage.py command-line interface")
        subparsers = parser.add_subparsers(dest="command")

        # runserver command
        runserver = subparsers.add_parser("runserver", help="Run the server")
        runserver.add_argument(
            "-b", "--bind", help="select the socket to bind. like -> [127.0.0.1:8000]"
        )
        # startapp command
        startapp = subparsers.add_parser("startapp", help="Create a new app")
        startapp.add_argument("name", help="name of the app")

        # createsuperuser command
        subparsers.add_parser("createsuperuser", help="Create a new super user")

        return parser

    @staticmethod
    def get_script():
        parser = ManagementUtility.createparser()
        args = parser.parse_args()

        if args.command == "runserver":
            bind = args.bind or "127.0.0.1:8000"
            ManagementUtility.runserver(bind=bind)

        elif args.command == "startapp":
            name = args.name
            ManagementUtility.startapp(name=name)
        else:
            parser.print_help()

    @classmethod
    def runserver(cls, bind):
        print("Runnig serever ...")
        command = ["gunicorn", "source.server:wsgi", f"-b {bind}"]
        subprocess.run(command)

    @classmethod
    def startapp(cls, name):
        if name in APPS:
            raise Exception(f"ERROR -> {name} app already exists!")
        path = BASE_DIR / name

        if not os.path.exists(path=path):
            os.makedirs(path)

            init_filename = path / "__init__.py"
            os.makedirs(os.path.dirname(init_filename), exist_ok=True)
            with open(init_filename, "x"):
                pass
            models_filename = path / "models.py"
            os.makedirs(os.path.dirname(models_filename), exist_ok=True)
            with open(models_filename, "x"):
                pass
            urls_filename = path / "urls.py"
            os.makedirs(os.path.dirname(urls_filename), exist_ok=True)
            with open(urls_filename, "w") as f:
                f.write(f"\napp_name = '{name}'\n")
                f.write(f"\n{name}_urls = {{}}\n")
            views_filename = path / "views.py"
            os.makedirs(os.path.dirname(views_filename), exist_ok=True)
            with open(views_filename, "x"):
                pass

        else:
            raise Exception(
                f"ERROR -> There is a directory with the same name as your app!"
            )
        # filename = "/foo/bar/baz.txt"
        # os.makedirs(os.path.dirname(filename), exist_ok=True)
        # with open(filename, "w") as f:
        #     f.write("FOOBAR")

    @classmethod
    def createsuperuser(cls):
        print("Create a super user ...")
