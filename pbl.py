# Used built-in module for date handling
from datetime import datetime
from abc import ABC, abstractmethod

# ==============================================================================
# 1. AUTHENTICATION & ROLE MANAGEMENT MODULE
# Ensures secure login for Students, Placement Admins, and Company Recruiters[span_1](start_span)[span_1](end_span).
# Demonstrates OOP Abstraction and Inheritance.
# ==============================================================================
class User(ABC):
    def __init__(self, user_id: int, username: str, role: str):
        self.user_id = user_id
        self.username = username
        self.role = role

    @abstractmethod
    def access_dashboard(self):
        pass

class StudentUser(User):
    def __init__(self, user_id: int, username: str):
        super().__init__(user_id, username, "Student")

    def access_dashboard(self):
        print(f"\n--- Welcome to the Student Dashboard, {self.username} ---")

class AdminUser(User):
    def __init__(self, user_id: int, username: str):
        super().__init__(user_id, username, "Placement Admin")

    def access_dashboard(self):
        print(f"\n--- Welcome to the Admin Dashboard, {self.username} ---")

class RecruiterUser(User):
    def __init__(self, user_id: int, username: str):
        super().__init__(user_id, username, "Company Recruiter")
        
    def access_dashboard(self):
        print(f"\n--- Welcome to the Recruiter Dashboard, {self.username} ---")


# ==============================================================================
# 2. STUDENT RECORD HANDLING MODULE
# Allows students to maintain digital resumes, CGPA, and technical skills[span_2](start_span)[span_2](end_span).
# Demonstrates OOP Encapsulation.
# ==============================================================================
class StudentRecord:
    def __init__(self, student_user: StudentUser, roll_no: str, current_cgpa: float):
        self.student = student_user
        self.roll_no = roll_no
        self.current_cgpa = current_cgpa
        self.technical_skills = []
        self.has_active_backlogs = False
        
    # Function with conditions
    def update_cgpa(self, new_cgpa: float):
        if 0.0 <= new_cgpa <= 10.0:
            self.current_cgpa = new_cgpa
            print(f"CGPA updated to {self.current_cgpa}")
        else:
            print("Invalid CGPA entered.")

    def add_skill(self, skill: str):
        self.technical_skills.append(skill)


# ==============================================================================
# 3. DRIVE MANAGEMENT ENGINE MODULE
# Hub to post company visits, specify job roles, package details (CTC), and eligibility[span_3](start_span)[span_3](end_span).
# ==============================================================================
class PlacementDrive:
    def __init__(self, company_name: str, job_role: str, package_ctc: float, min_cgpa: float, no_backlogs_required: bool):
        self.company_name = company_name
        self.job_role = job_role
        self.package_ctc = package_ctc
        self.min_cgpa = min_cgpa
        self.no_backlogs_required = no_backlogs_required
        self.drive_date = datetime.now().strftime("%Y-%m-%d")

    # Function with conditions to check eligibility rules[span_4](start_span)[span_4](end_span)
    def check_eligibility(self, student_record: StudentRecord) -> bool:
        if student_record.current_cgpa < self.min_cgpa:
            return False
        if self.no_backlogs_required and student_record.has_active_backlogs:
            return False
        return True


# ==============================================================================
# 4. APPLICATION & TRACKING SYSTEM MODULE
# Students view matching drives, apply, and track journey stages[span_5](start_span)[span_5](end_span).
# Demonstrates loops and conditional logic.
# ==============================================================================
class TrackingSystem:
    # Valid tracking stages: Applied, Shortlisted, Interviewing, and Placed[span_6](start_span)[span_6](end_span)
    VALID_STAGES = ["Applied", "Shortlisted", "Interviewing", "Placed"]

    def __init__(self):
        self.applications = []

    def apply_for_drive(self, student_record: StudentRecord, drive: PlacementDrive):
        """Simulates single-click apply for matching drives."""
        if drive.check_eligibility(student_record):
            application = {
                "student": student_record.student.username,
                "company": drive.company_name,
                "role": drive.job_role,
                "status": self.VALID_STAGES[0] # Defaults to "Applied"
            }
            self.applications.append(application)
            print(f"Success: {student_record.student.username} successfully applied to {drive.company_name}.")
        else:
            print(f"Eligibility Error: {student_record.student.username} does not meet requirements for {drive.company_name}.")

    def view_student_journey(self, student_name: str):
        """Uses a loop to track the journey across multiple stages."""
        print(f"\n--- Placement Tracking Journey for {student_name} ---")
        found = False
        
        # Loop to iterate through tracking records
        for app in self.applications:
            if app["student"] == student_name:
                found = True
                print(f"Company: {app['company']} | Role: {app['role']} | Status: {app['status']}")
                
        if not found:
            print("No applications found.")


# ==============================================================================
# MAIN EXECUTION (Simulating the Program)
# ==============================================================================
if __name__ == "__main__":
    # 1. Initialize Authentication / Users
    admin = AdminUser(1, "Placement_Coordinator")
    student1 = StudentUser(101, "Shivam Kumar")
    
    admin.access_dashboard()
    student1.access_dashboard()

    # 2. Setup Student Records
    shivam_record = StudentRecord(student1, "CSE202601", 8.8)
    shivam_record.add_skill("Python")
    shivam_record.add_skill("Flask")

    # 3. Setup Drive Management Engine
    google_drive = PlacementDrive("Google", "Software Engineer", 28.0, 8.5, True)
    tcs_drive = PlacementDrive("TCS", "System Engineer", 7.0, 6.0, False)
    microsoft_drive = PlacementDrive("Microsoft", "SDE-1", 24.0, 9.0, True) # Shivam is 8.8, Microsoft needs 9.0

    # 4. Process Applications and Tracking
    tracking_system = TrackingSystem()
    print("\n--- Applying for Drives ---")
    tracking_system.apply_for_drive(shivam_record, google_drive)
    tracking_system.apply_for_drive(shivam_record, tcs_drive)
    tracking_system.apply_for_drive(shivam_record, microsoft_drive) # Will fail condition

    # Update a status to simulate tracking stages[span_7](start_span)[span_7](end_span)
    tracking_system.applications[0]["status"] = TrackingSystem.VALID_STAGES[2] # Moving to "Interviewing"
    
    # View final journey
    tracking_system.view_student_journey("Shivam Kumar")
