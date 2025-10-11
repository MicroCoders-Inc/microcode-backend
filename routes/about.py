from . import api_bp


@api_bp.route("/about")
def handleAbout():
    return {"msg": "Hola mundo desde About en el backend!"}
