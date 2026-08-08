import uuid


class SessionManager:

    @staticmethod
    def create_session():

        return str(uuid.uuid4())


session_manager = SessionManager()