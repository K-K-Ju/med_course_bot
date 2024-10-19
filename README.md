# Telegram bot for medicine school

Telegram bot which performs giving essential information about school and apply students for the lessons. Also this bot has admin panel for managering applies and users. 

## Installation and configuration

Install all dependencies:

```sh
python3 -m pip install -r requirements.txt
```
Provide all keys for Pyrogram client (api_hash, api_id, bot_api)
```python
AppClient(name="Med School Bot", lang='ua', api_id=12345678, api_hash='your_app_hash', bot_api='1234567:your_bot_api')
```
> Note: after first launch Pyrogrma generaes session file which is loaded each app start, so you don`t need to remain sensible data in code.

App is using .json config file.

## Usage example


_For more examples and usage, please refer to the [Wiki][wiki]._

## Running

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
python3 bot/main.py path/to/config.json
```

## Meta

Your Name – [@LinkedIn](https://www.linkedin.com/in/andrii-prodan-1513ba234/) – coderinhat@aol.com

Distributed under the GPL-3.0 license. See ``LICENSE`` for more information.

[LICENSE](https://github.com/K-K-Ju/med_course_bot/blob/master/LICENSE.txt)

