from flask import Flask, make_response, send_from_directory, request
from feedgen.feed import FeedGenerator
from episodio import Episodios
import pathlib, os

app = Flask(__name__)



NAME = "your name"
EMAIL = "your email"
PODCAST_TITLE = "your podcast title"
PODCAST_SUBTITLE = "your podcast description"
PODCAST_CATEGORY = "your podcast category"

IMAGE_DIR = "."
BOOK_DIR = pathlib.Path("audio")
SERVER_HOME = "http://127.0.0.1:5000"


@app.route("/")
def home():
    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.title(PODCAST_TITLE)
    fg.author({"name": NAME, "email": EMAIL})
    fg.logo(f"{SERVER_HOME}/public/img/logo.jpg")
    fg.subtitle(PODCAST_SUBTITLE)
    fg.language("pt")
    fg.link(href=SERVER_HOME)
    fg.podcast.itunes_author(NAME)
    fg.podcast.itunes_category(
        [
            {"cat": "Book", "sub": PODCAST_CATEGORY},
        ]
    )
    fg.podcast.itunes_complete("yes")
    fg.podcast.itunes_image(f"{SERVER_HOME}/public/img/logo.jpg")
    fg.podcast.itunes_subtitle(PODCAST_SUBTITLE)
    obj_eps = Episodios()
    eps = obj_eps.ver_episodios()
    for row in eps:
        if len(row) > 0:
            fe = fg.add_entry()
            fe.id(f"{SERVER_HOME}/public/audio/{row[2]}.aac")
            fe.title(str(row[0]))
            fe.description(str(row[1]))
            fe.enclosure(
                f"{SERVER_HOME}/public/audio/{row[2]}.aac",
                str(os.path.getsize(f"public/audio/{row[2]}.aac")),
                "audio/aac",
            )
    response = make_response(fg.rss_str(pretty=True))
    response.headers.set("Content-Type", "application/rss+xml; charset=utf-8")
    return response


@app.route("/adicionar-episodio", methods=["POST"])
def adicionar_ep():
    obj_eps = Episodios()
    api_key = request.headers.get("x-api-key")
    nome_ep = request.headers.get("name-ep")
    desc_ep = request.headers.get("desc-ep")
    nome_ficheiro = request.headers.get("name-file")
    ficheiro = request.data
    if obj_eps.submeter_episodio(
        api_key=api_key,
        nome_ep=nome_ep,
        desc_ep=desc_ep,
        nome_ficheiro=nome_ficheiro,
        ficheiro=ficheiro,
    ):
        return make_response(str(200), 200)
    else:
        return make_response(str(401), 401)


@app.route("/public/<path:path>")
def send_public(path):
    return send_from_directory("public", path)
