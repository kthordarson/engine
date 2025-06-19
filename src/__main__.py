from .docs import *
from .project import *

# fix namespace problems
from .docs import build as docs_build
from .examples import run as examples_run

import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="pyxora",
        description="pyxora CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to run")

    # new
    parser_new = subparsers.add_parser("new", help="Create a new project")
    parser_new.add_argument("project_name", help="The name of the new project")
    parser_new.set_defaults(func=new)

    # open
    parser_open = subparsers.add_parser("open", help="Open a project")
    parser_open.add_argument("project_name", help="The name of the project to open")
    parser_open.set_defaults(func=open)

    # run
    parser_run = subparsers.add_parser("run", help="Run a project")
    parser_run.add_argument("project_name", help="The name of the new project")
    parser_run.set_defaults(func=run)

    # delete
    parser_delete = subparsers.add_parser("delete", help="Delete a project")
    parser_delete.add_argument("project_name", help="The name of the project to delete")
    parser_delete.set_defaults(func=delete)

    # build
    parser_build = subparsers.add_parser("build", help="Build a project")
    parser_build.add_argument("project_name", help="The name of the project to build")
    parser_build.set_defaults(func=build)

    # info
    parser_info = subparsers.add_parser("info", help="Show info about a project")
    parser_info.add_argument("project_name", help="The name of the project")
    parser_info.set_defaults(func=info)

    # list
    parser_list = subparsers.add_parser("list", help="List all projects")
    parser_list.set_defaults(func=list)

    # docs with subcommands: run, build, online
    parser_docs = subparsers.add_parser("docs", help="Project documentation")
    docs_subparsers = parser_docs.add_subparsers(
        dest="doc options", required=True, help="Docs options"
    )

    # docs run
    parser_docs_run = docs_subparsers.add_parser("local", help="Run docs server locally")
    parser_docs_run.set_defaults(func=local)

    # docs build
    parser_docs_build = docs_subparsers.add_parser("build", help="Build the documentation")
    parser_docs_build.set_defaults(func=docs_build)

    # docs online
    parser_docs_online = docs_subparsers.add_parser("online", help="Open online documentation")
    parser_docs_online.set_defaults(func=online)

    # examples
    parser_examples = subparsers.add_parser("examples", help="Run or list example projects")
    parser_examples.add_argument("example_name", nargs="?", help="Name of the example to run")
    parser_examples.set_defaults(func=examples_run)

    args = parser.parse_args()

    args.func(args)

if __name__ == "__main__":
    main()
