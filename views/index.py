import smrti_quant_website


@smrti_quant_website.app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
