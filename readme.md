# Discord Friend Timezones

A small Discord timezones bot for keeping track of other users' timezones and local times.

You can invite the bot [here](https://discordapp.com/oauth2/authorize?client_id=661969491407798303&permissions=0&scope=bot)
or host it yourself.



## Features

- Each user sets their timezone with `--tzset <timezone>`. 
This supports fuzzy matching, so you can set it to `Europe/London` with `--tzset london` for example.
- View users' timezones with `--tzget <list of mentions>`.
- View users' local times with `--time <list of mentions>`.

## Self-Hosting

You need at least Python 3.6 installed. It is also recommended to use a virtualenv. 

- Clone this repo
- Install requirements using `pip install -r requirements.txt`
- Create a file called `settings.json` inside the cloned directory, this should contain the following:

```json
{
  "token": "your bot token",
  "prefix": "--",
  "database": "sqlite:///database.db"
}
```

> These are example values, any prefix or database URI can be used.

- Run `python bot.py`
