# Getting started

## Install Python

You'll need Python version 3.12 or newer.

TODO: links for installing python on Windows, Mac, Linux.

### Install `uv` for managing virtual environments

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Install opencode


```
curl -fsSL https://opencode.ai/install | bash
```

Alternatively, there is a snap version:

```
sudo snap install opencode
```

If you already have Node, this also works:

```
npm install -g opencode-ai
```

### Copy the opencode config file

Take the `opencode.json` file from the setup/ directory and copy it to `~/.config/opencode/opencode.json`

You should have received a mail with an api key. Put that api key into the opencode.json file in the `apiKey` field.

### Start opencode

Run `opencode` from the commandline. Type `/models` and scroll through the list of models. You should see a model called `infomaniak-kimi`, among others.

Exit opencode with `ctrl-c` or `ctrl-d`.

### Optional: visit the llm proxy website 

The email with the api token also contained an invite link. This lets you create an account where you can see the litellm proxy. 
This lets you track your request and token usage.

