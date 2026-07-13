from app.controllers.student_controller import StudentController


class FacultyController:
    def __init__(self, student_controller=None):
        self.student_controller = student_controller or StudentController()

    def dashboard(self):
        return self.student_controller.dashboard()
