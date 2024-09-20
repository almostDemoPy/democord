# democord
A Python library for the Discord API


![Static Badge](https://img.shields.io/badge/demo.py-4584b6)
![Static Badge](https://img.shields.io/badge/version-0.9b6-yellow)
![GitHub Created At](https://img.shields.io/github/created-at/almostDemoPy/democord?style=flat)
![Discord](https://img.shields.io/discord/1267703591863586858?style=flat)
![GitHub License](https://img.shields.io/github/license/almostDemoPy/democord)


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Z8Z413A7I5)


![Static Badge](https://img.shields.io/badge/Python_%3E%3D3.12-ffde57?style=for-the-badge&logo=python)
![Static Badge](https://img.shields.io/badge/Discord_API-586582?style=for-the-badge&logo=discord)


---

## Quickstart
```py
from democord import App, Intents

app : App = App(
  intents = Intents.default()
)

@app.event
async def on_ready() -> None:
  print("bot is online")

app.run()
```

---

## Manuals
Welcome to the Wiki of the democord Discord API library. The wiki showcases classes and functions that are available to you.

\- [democord API Reference](https://github.com/almostDemoPy/democord/wiki/Core-API-Reference#table-of-contents)

---

## Sponsorships

Sponsor us ( or me... ._. i'm lonely ) and help maintain the library ( and my sanity ) :

- [ko-fi.com/demopy](<https://ko-fi.com/demopy>)

---

## Socials

**Discord** : [democord](<https://discord.gg/xkYmzuwMFv>)