from . import api_bp


@api_bp.route("/contact")
def handleContact():
    return {"msg": "Hola mundo desde Contact en el backend!"}
