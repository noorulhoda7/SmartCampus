from werkzeug.exceptions import Forbidden, InternalServerError, NotFound


def register_error_handlers(flask_app):
    @flask_app.errorhandler(Forbidden)
    def handle_forbidden(error):
        flask_app.logger.warning("Forbidden request: %s", error)
        return "Forbidden", 403

    @flask_app.errorhandler(NotFound)
    def handle_not_found(error):
        flask_app.logger.info("Page not found: %s", error)
        return "Page not found", 404

    @flask_app.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        original_error = getattr(error, "original_exception", None)
        if original_error:
            flask_app.logger.exception("Internal server error", exc_info=original_error)
        else:
            flask_app.logger.exception("Internal server error")
        return "Internal server error", 500

    @flask_app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        flask_app.logger.exception("Unexpected application error")
        return "Internal server error", 500
