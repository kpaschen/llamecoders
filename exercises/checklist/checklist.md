# Are you ready to code?

## Commandline

Some of the steps below ask you to open a commandline prompt.
In Windows, use powershell.
In Linux or Mac, any terminal with a shell will do.

## Python

You should have installed Python as part of the preparation; if you haven't, please do it now.

In the commandline window, type `python` or `python3`.

You should get a prompt that looks like this:

```
Python 3.12.3 (main, Jul 15 2026, 23:46:41) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

You get out back to the commandline with `quit()` or `Ctrl-D`.

## Git

You should have installed a git client as part of the preparation; if you haven't, please do it now.

In your commandline window, type `git status`. You should get a reply saying you are not in a git repository.

Create a directory for the coursework and switch to it in your shell, then

```
git clone <coursework repository>
```

## IDE or Editor

If you already have an IDE or a preferred editor, you are welcome to keep using it. Otherwise, please read on.

`vscode` aka Visual Studio Code is a development environment created by Microsoft that is free for personal use. It is popular
and supports a variety of modern programming languages, including Python. It is a good default choice.

If you do not want to install vscode, any text editor will do. On Windows, notepad works. On Linux, nano is a popular choice.

Open your IDE or editor of choice, create a file called `hello.py` with the contents

```
print("Hello World!")
```

Save it, then run `python hello.py`. You should get the output `Hello World!`.

## Opencode

You should have installed opencode as part of the preparation; if you haven't, please do it now.

Copy the opencode.json from our repository, insert your key, then start opencode:

`opencode`

You should get a screen with some orange and white text. Type

`models` to get a list of available models. Some of them are marked as `Free` (they come with opencode), some have names that start with `infomaniak-`, those are available through our proxy. Choose one of the free models for now.

Once you have chosen a model, type `hello`. You should get a reply, possibly after a second or two.

# All good?

Congratulations, this concludes the checklist. If you have any questions, please ask.
