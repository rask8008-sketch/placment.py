from datetime import datetime
import streamlit as st
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# ==============================================================================
# 1. AUTHENTICATION & ROLE MANAGEMENT MODULE
# ==============================================================================
class User(ABC):
    def __init__(self, user_id: int, username: str, role: str):
        self.user_id = user_id
        self.username = username
        self.role = role

    @abstractmethod
    def get_welcome_message(self) -> str:
        pass

class StudentUser(User):
    def __init__(self, user_id: int, username: str):
        super().__init__(user_id, username, "Student")

    def get_welcome_message(self) -> str:
        return f"Welcome to the Student Dashboard, {self.username}"

class AdminUser(User):
    def __init__(self, user_id: int, username: str):
        super().__init__(user_id, username, "Placement Admin")

    def get_welcome_message(self) -> str:
        return f"Welcome to the Admin Dashboard, {self.username}"

class RecruiterUser(User):
    def __init__(self, user_id: int, username: str):
        super().__init__(user_id, username, "Company Recruiter")
        
    def get_welcome_message(self) -> str:
        return f"Welcome to the Recruiter Dashboard, {self.username}"


# ==============================================================================
# 2. STUDENT RECORD HANDLING MODULE
# ==============================================================================
class StudentRecord:
    def __init__(self, student_user: StudentUser, roll_no: str, current_cgpa: float):
        self.student = student_user
        self.roll_no = roll_no
        self.current_cgpa = current_cgpa
        self.technical_skills: List[str] = []
        self.has_active_backlogs = False
        
    def update_cgpa(self, new_cgpa: float) -> tuple[bool, str]:
        if 0.0 <= new_cgpa <= 10.0:
            self.current_cgpa = new_cgpa
            return True, f"CGPA updated successfully to {self.current_cgpa}"
        return False, "Invalid CGPA entered. Must be between 0.0 and 10.0."

    def add_skill(self, skill: str) -> bool:
        clean_skill = skill.strip()
        if clean_skill and clean_skill.lower() not in [s.lower() for s in self.technical_skills]:
            self.technical_skills.append(clean_skill)
            return True
        return False


# ==============================================================================
# 3. DRIVE MANAGEMENT ENGINE MODULE
# ==============================================================================
class PlacementDrive:
    def __init__(self, drive_id: int, company_name: str, job_role: str, package_ctc: float, min_cgpa: float, no_backlogs_required: bool):
        self.drive_id = drive_id
        self.company_name = company_name
        self.job_role = job_role
        self.package_ctc = package_ctc
        self.min_cgpa = min_cgpa
        self.no_backlogs_required = no_backlogs_required
        self.drive_date = datetime.now().strftime("%Y-%m-%d")

    def check_eligibility(self, student_record: StudentRecord) -> tuple[bool, str]:
        if student_record.current_cgpa < self.min_cgpa:
            return False, f"Minimum CGPA required is {self.min_cgpa} (Your CGPA: {student_record.current_cgpa})"
        if self.no_backlogs_required and student_record.has_active_backlogs:
            return False, "Active backlogs are not allowed for this drive."
        return True, "Eligible"


# ==============================================================================
# 4. APPLICATION & TRACKING SYSTEM MODULE
# ==============================================================================
class TrackingSystem:
    VALID_STAGES = ["Applied", "Shortlisted", "Interviewing", "Placed"]

    def __init__(self):
        self.drives: Dict[int, PlacementDrive] = {}
        self.applications: List[Dict[str, Any]] = []

    def register_drive(self, drive: PlacementDrive):
        self.drives[drive.drive_id] = drive

    def apply_for_drive(self, student_record: StudentRecord, drive: PlacementDrive) -> tuple[bool, str]:
        is_eligible, reason = drive.check_eligibility(student_record)
        
        if not is_eligible:
            return False, f"Eligibility Error: {student_record.student.username} does not meet requirements ({reason})."

        # Check if already applied
        for app in self.applications:
            if app["student_id"] == student_record.student.user_id and app["drive_id"] == drive.drive_id:
                return False, "You have already applied for this drive."

        application = {
            "student_id": student_record.student.user_id,
            "student_name": student_record.student.username,
            "drive_id": drive.drive_id,
            "company": drive.company_name,
            "role": drive.job_role,
            "status": self.VALID_STAGES[0]
        }
        self.applications.append(application)
        return True, f"Success: {student_record.student.username} successfully applied to {drive.company_name}!"

    def update_application_status(self, student_id: int, drive_id: int, new_status: str) -> bool:
        for app in self.applications:
            if app["student_id"] == student_id and app["drive_id"] == drive_id:
                app["status"] = new_status
                return True
        return False


# ==============================================================================
# 5. STREAMLIT CONFIGURATION & INITIAL STATE
# ==============================================================================
st.set_page_config(page_title="Placement Portal", page_icon="🎓", layout="wide")

def init_session():
    if "initialized" not in st.session_state:
        admin = AdminUser(1, "Placement_Coordinator")
        student1 = StudentUser(101, "Shivam Kumar")
        student2 = StudentUser(102, "Asha Verma")
        recruiter = RecruiterUser(201, "Google Recruiter")

        shivam_record = StudentRecord(student1, "CSE202601", 8.8)
        shivam_record.add_skill("Python")
        shivam_record.add_skill("Flask")

        asha_record = StudentRecord(student2, "CSE202602", 7.2)
        asha_record.has_active_backlogs = True
        asha_record.add_skill("Java")

        tracking_system = TrackingSystem()
        
        # Adding sample drives
        d1 = PlacementDrive(1, "Google", "Software Engineer", 28.0, 8.5, True)
        d2 = PlacementDrive(2, "TCS", "System Engineer", 7.0, 6.0, False)
        d3 = PlacementDrive(3, "Microsoft", "SDE-1", 24.0, 9.0, True)

        tracking_system.register_drive(d1)
        tracking_system.register_drive(d2)
        tracking_system.register_drive(d3)

        # Pre-apply Shivam to Google & TCS to mirror script
        tracking_system.apply_for_drive(shivam_record, d1)
        tracking_system.apply_for_drive(shivam_record, d2)

        st.session_state.students = {101: shivam_record, 102: asha_record}
        st.session_state.admin = admin
        st.session_state.recruiter = recruiter
        st.session_state.tracking = tracking_system
        st.session_state.next_drive_id = 4
        st.session_state.initialized = True

init_session()

tracking_system: TrackingSystem = st.session_state.tracking

# ==============================================================================
# SIDEBAR: NAVIGATION & ROLE SWITCHER
# ==============================================================================
st.sidebar.title("🎓 Campus Placement Portal")
st.sidebar.markdown("---")

role_selected = st.sidebar.selectbox(
    "Select Role / View:",
    ["Student (Shivam Kumar)", "Student (Asha Verma)", "Company Recruiter", "Placement Admin"]
)

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Portal Data"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ==============================================================================
# VIEW 1: STUDENT DASHBOARD
# ==============================================================================
if role_selected.startswith("Student"):
    student_id = 101 if "Shivam" in role_selected else 102
    current_record: StudentRecord = st.session_state.students[student_id]

    st.title(f"👨‍🎓 {current_record.student.get_welcome_message()}")
    st.caption(f"Roll No: **{current_record.roll_no}** | ID: {current_record.student.user_id}")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📋 My Profile")
        with st.container(border=True):
            st.metric("Current CGPA", f"{current_record.current_cgpa} / 10.0")
            st.write(f"**Backlog Status:** {'⚠️ Active Backlogs' if current_record.has_active_backlogs else '✅ Clean (No Backlogs)'}")
            st.write(f"**Technical Skills:** {', '.join(current_record.technical_skills) if current_record.technical_skills else 'None'}")

        with st.expander("⚙️ Update Details"):
            new_cgpa = st.number_input("Update CGPA", 0.0, 10.0, float(current_record.current_cgpa), 0.1)
            backlog_flag = st.checkbox("Active Backlogs?", value=current_record.has_active_backlogs)
            if st.button("Save Profile"):
                ok, msg = current_record.update_cgpa(new_cgpa)
                current_record.has_active_backlogs = backlog_flag
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

            st.divider()
            new_skill = st.text_input("Add Skill")
            if st.button("Add"):
                if current_record.add_skill(new_skill):
                    st.success(f"Added {new_skill}")
                    st.rerun()
                else:
                    st.warning("Invalid or duplicate skill.")

    with col2:
        st.subheader("🚀 Available Placement Drives & Applications")
        
        # Tabs for drives vs applied journey
        tab_drives, tab_journey = st.tabs(["Active Drives", "My Tracking Journey"])

        with tab_drives:
            for d_id, drive in tracking_system.drives.items():
                is_elig, reason = drive.check_eligibility(current_record)
                
                # Check application status
                applied_app = next((app for app in tracking_system.applications if app["student_id"] == student_id and app["drive_id"] == d_id), None)

                with st.container(border=True):
                    c_a, c_b = st.columns([3, 1])
                    with c_a:
                        st.markdown(f"### {drive.company_name} — *{drive.job_role}*")
                        st.write(f"💰 **CTC:** ₹{drive.package_ctc} LPA | 📊 **Min CGPA:** {drive.min_cgpa} | 🚫 **Backlogs Allowed:** {'Yes' if not drive.no_backlogs_required else 'No'}")
                        st.caption(f"Drive Date: {drive.drive_date}")
                    
                    with c_b:
                        st.write("")
                        if applied_app:
                            st.info(f"Status: **{applied_app['status']}**")
                        elif is_elig:
                            if st.button("Apply Now", key=f"apply_{d_id}_{student_id}", type="primary"):
                                success, msg = tracking_system.apply_for_drive(current_record, drive)
                                if success:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                        else:
                            st.error("Not Eligible")
                            st.caption(reason)

        with tab_journey:
            st.markdown(f"#### Placement Journey Tracker for {current_record.student.username}")
            student_apps = [app for app in tracking_system.applications if app["student_id"] == student_id]
            
            if not student_apps:
                st.info("No applications found.")
            else:
                for app in student_apps:
                    with st.container(border=True):
                        st.write(f"🏢 **Company:** {app['company']} | 💼 **Role:** {app['role']}")
                        
                        # Visual progress representation of stages
                        current_status = app["status"]
                        cols = st.columns(len(TrackingSystem.VALID_STAGES))
                        for idx, stage in enumerate(TrackingSystem.VALID_STAGES):
                            with cols[idx]:
                                if stage == current_status:
                                    st.markdown(f"🟢 **[{stage}]**")
                                elif TrackingSystem.VALID_STAGES.index(stage) < TrackingSystem.VALID_STAGES.index(current_status):
                                    st.markdown(f"✅ {stage}")
                                else:
                                    st.markdown(f"⚪ {stage}")

# ==============================================================================
# VIEW 2: COMPANY RECRUITER DASHBOARD
# ==============================================================================
elif role_selected == "Company Recruiter":
    recruiter: RecruiterUser = st.session_state.recruiter
    st.title(f"🏢 {recruiter.get_welcome_message()}")

    tab_post, tab_manage = st.tabs(["Post New Drive", "Manage Applications & Status"])

    with tab_post:
        st.subheader("Post a New Company Drive")
        with st.form("drive_form"):
            comp_name = st.text_input("Company Name", "Amazon")
            job_role = st.text_input("Job Role", "Cloud Support Engineer")
            ctc = st.number_input("Package CTC (LPA)", value=18.0)
            min_cgpa = st.slider("Minimum CGPA", 0.0, 10.0, 7.5, 0.1)
            no_backlogs = st.checkbox("Strictly No Backlogs Allowed?", value=True)

            submitted = st.form_submit_button("Publish Drive", type="primary")
            if submitted:
                new_drive = PlacementDrive(
                    drive_id=st.session_state.next_drive_id,
                    company_name=comp_name,
                    job_role=job_role,
                    package_ctc=ctc,
                    min_cgpa=min_cgpa,
                    no_backlogs_required=no_backlogs
                )
                tracking_system.register_drive(new_drive)
                st.session_state.next_drive_id += 1
                st.success(f"Drive for {comp_name} published successfully!")

    with tab_manage:
        st.subheader("Update Student Tracking Stages")
        if not tracking_system.applications:
            st.info("No active applications to manage.")
        else:
            for app in tracking_system.applications:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([2, 2, 2])
                    with c1:
                        st.write(f"**Student:** {app['student_name']}")
                        st.write(f"**Company:** {app['company']} ({app['role']})")
                    with c2:
                        st.write(f"**Current Stage:** `{app['status']}`")
                    with c3:
                        new_stage = st.selectbox(
                            "Change Stage",
                            TrackingSystem.VALID_STAGES,
                            index=TrackingSystem.VALID_STAGES.index(app['status']),
                            key=f"status_{app['student_id']}_{app['drive_id']}"
                        )
                        if new_stage != app['status']:
                            tracking_system.update_application_status(app['student_id'], app['drive_id'], new_stage)
                            st.success("Updated!")
                            st.rerun()

# ==============================================================================
# VIEW 3: PLACEMENT ADMIN DASHBOARD
# ==============================================================================
elif role_selected == "Placement Admin":
    admin: AdminUser = st.session_state.admin
    st.title(f"🛡️ {admin.get_welcome_message()}")

    m1, m2, m3 = st.columns(3)
    m1.metric("Registered Students", len(st.session_state.students))
    m2.metric("Total Placement Drives", len(tracking_system.drives))
    m3.metric("Total Applications", len(tracking_system.applications))

    st.divider()

    col_s, col_d = st.columns(2)
    with col_s:
        st.subheader("Student Database Records")
        s_list = []
        for sid, rec in st.session_state.students.items():
            s_list.append({
                "ID": sid,
                "Name": rec.student.username,
                "Roll No": rec.roll_no,
                "CGPA": rec.current_cgpa,
                "Backlogs": "Yes" if rec.has_active_backlogs else "No",
                "Skills": ", ".join(rec.technical_skills)
            })
        st.dataframe(s_list, use_container_width=True)

    with col_d:
        st.subheader("All Placement Drives")
        d_list = []
        for did, drive in tracking_system.drives.items():
            d_list.append({
                "ID": did,
                "Company": drive.company_name,
                "Role": drive.job_role,
                "CTC (LPA)": drive.package_ctc,
                "Min CGPA": drive.min_cgpa,
                "No Backlogs": "Yes" if drive.no_backlogs_required else "No"
            })
        st.dataframe(d_list, use_container_width=True)
