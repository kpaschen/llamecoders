# Getting started

## Install Python

You'll need Python version 3.12 or newer.

### Install Python on Windows

Open *PowerShell* or *Command Prompt* from the Start menu and type:

```
python --version
```

If this finds a python version that is at least 3.12, you're good, otherwise:

```
winget install Python.python.3.14
```

### Install Python on Linux or MacOS

In a shell, type `python --version` or `python3 --version`. If this
shows you a version 3.12 or newer, you've already got the right version of Python.

If you have an older version of Python, you can upgrade to a newer one. However, if you'd rather not do that (maybe you have other tools that need the older version), you can install additional versions. One reasonably 
easy way to do that is a tool called `uv`

#### Install `uv` for managing virtual environments and/or multiple versions of Python

This is essential if you need to manage multiple versions of python. It is generally useful for managing
dependencies.

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

You can now run

```
uv venv --python 3.12
source .venv/bin/activate
```

And then the shell where you ran this will be using python 3.12.

The [uv website](https://docs.astral.sh) has more information.

## Install opencode


```
curl https://opencode.ai/install -o opencode-installer.sh
# Inspect this script if you want to, then run:
bash opencode-installer.sh
```

Alternatively, there is a snap version:

```
sudo snap install opencode
```

If you already have Node, this also works:

```
npm install -g opencode-ai
```

Opencode comes in different versions, and they behave slightly differently. If you're on an older version 
(like 1.17) you may see failures when trying to access some of our models.

Opencode keeps a lot of cached information around in various places. Especially after an update or major changes, 
it can get confused. Stuff that previously worked will suddenly show you strange error message. When this happens, 
ask for help and we'll see what we can do. However, the easiest option tends to be uninstalling and reinstalling
opencode.

### Copy the opencode config file

Take the `opencode.json` file from the setup/ directory and copy it to `~/.config/opencode/opencode.json`

### Start opencode

You should have received a mail with an api key. Hang onto that key, but don't share it with anyone else.

On Linux and MacOS:

```
export LLM_API_KEY=the key from the mail
opencode
```

On Windows:

open powershell, then

```
$Env:LLM_API_KEY = the key from the mail
opencode
```

Now you've got opencode running in a terminal.  Type `/models` and scroll through the list of models. You should see a model called `infomaniak-kimi`, among others.

Exit opencode with `ctrl-c` or `ctrl-d`.

Other tools for interacting with LLMs exist, and you're welcome to use whatever works for you.

### Optional: visit the llm proxy website 

The email with the api token also contained an invite link. This lets you create an account where you can see the litellm proxy. 
This lets you track your request and token usage.

The proxy website has tabs for interacting with models, but they will not work for you. The proxy website
is really an admin dashboard. If you want a web ui, keep on reading:

#### Optional: Use Open Webui

If you have docker, you can run this locally:

```
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

This takes a while to start (check with `docker ps`). You can connect to `localhost:3000` and create a user. This user will be an admin. 

Click on the user icon in the bottom left, open `settings` then `connections`. These options all look greyed out but they are selectable. Add a connection to our litellm proxy with your credentials.
Now you can use the models by clicking in the top left (not by clicking on `workspaces`, for some reason).

This gives you a web ui sort of like what you'll have seen with ChatGPT.

### Optional: use LLMs from VS Code

Visual Studio Code is a free development environment that works with Python. It supports third-party `extensions`, and some of those support various kinds of LLM integration.

One that works with our setup is `continue.dev`. After installing this extension, start it. Where it wants you to choose/configure models, choose `local`, then `skip and configure manually`. This pops up an editor with 
a default config. There's a sample `continue config` in the `setup` directory of this repo.
