import logging

import connexion


if __name__ == "__main__":
    logging.root.setLevel(logging.DEBUG)

    app = connexion.App(
        __name__, specification_dir="./resources/")
    app.add_api("swagger.yaml")
    app.run(port=8080)
