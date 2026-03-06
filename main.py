import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os
import random

# --- Theme Configuration ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HospitaKrEnterprise(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("1350x850")
        self.configure(fg_color="#0F172A") 
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.db_init()
        self.setup_ui_skeleton()
        self.show_login_screen()

    def db_init(self):
        self.conn = sqlite3.connect('hospita_pro_v4.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
        self.cur.execute('''CREATE TABLE IF NOT EXISTS patients (
            pid TEXT PRIMARY KEY, name TEXT, date_in TEXT, doctor TEXT, 
            disease TEXT, status TEXT, room TEXT, bill REAL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS staff (
            sid TEXT PRIMARY KEY, name TEXT, role TEXT, specialty TEXT, bio TEXT)''')

        if not self.cur.execute("SELECT * FROM users WHERE username='admin'").fetchone():
            self.cur.execute("INSERT INTO users VALUES (?,?)", ("admin", "1234"))

        # --- REFRESH STAFF (15 Doctors + 30 Staff) ---
        self.cur.execute("DELETE FROM staff")
        doctors_list = [
            ("D-1", "Dr. Sameer Iyer", "Doctor", "Neurosurgeon", "Neuro-mapping expert."),
            ("D-2", "Dr. Aditi Sharma", "Doctor", "Cardiologist", "Pediatric heart specialist."),
            ("D-3", "Dr. Rajesh Khanna", "Doctor", "Oncologist", "Chemotherapy lead."),
            ("D-4", "Dr. Meera Deshmukh", "Doctor", "Gynecologist", "Robotic surgery specialist."),
            ("D-5", "Dr. Vikram Malhotra", "Doctor", "Orthopedic", "Joint replacement expert."),
            ("D-6", "Dr. Sanya Gupta", "Doctor", "Dermatologist", "Laser surgery specialist."),
            ("D-7", "Dr. Arjun Reddy", "Doctor", "Psychiatrist", "Behavioral therapy lead."),
            ("D-8", "Dr. Neha Kapoor", "Doctor", "Pediatrician", "Neonatal care expert."),
            ("D-9", "Dr. Rohan Varma", "Doctor", "Urologist", "Kidney stone specialist."),
            ("D-10", "Dr. Ishani Roy", "Doctor", "Endocrinologist", "Diabetes management."),
            ("D-11", "Dr. Kabir Singh", "Doctor", "General Surgeon", "Trauma specialist."),
            ("D-12", "Dr. Preeti Saini", "Doctor", "Radiologist", "Imaging expert."),
            ("D-13", "Dr. Armaan Malik", "Doctor", "Rheumatologist", "Autoimmune lead."),
            ("D-14", "Dr. Zoya Ali", "Doctor", "Pulmonologist", "Lung transplant specialist."),
            ("D-15", "Dr. Manav Kaul", "Doctor", "ENT Specialist", "Cochlear implant expert.")
        ]
        
        s_names = ["Anjali Menon", "Rahul Verma", "Suresh Raina", "Priya Mani", "Amit Mishra", 
                   "Sneha Rao", "Karan Johar", "Lata Hegde", "Vijay Seth", "Deepa Malik", 
                   "Ravi Teja", "Monica G", "Sanjay Dutt", "Alia Bhatt", "Varun Dhawan", 
                   "Ranbir K", "Kiara A", "Sid M", "Pooja Hegde", "Prabhas R", 
                   "Shraddha K", "Tiger Shroff", "Kriti Sanon", "Ayushmann K", "Vicky Kaushal", 
                   "Sara Ali", "Kartik A", "Janhvi K", "Ishaan K", "Ananya P"]
        roles = ["Nurse", "Technician", "Admin", "Pharmacist"]
        support_staff = [(f"S-{i+1}", s_names[i], random.choice(roles), f"{random.choice(roles)} Dept", "Hospital Staff") for i in range(30)]
        self.cur.executemany("INSERT INTO staff VALUES (?,?,?,?,?)", doctors_list + support_staff)

        # --- INJECT 50 PATIENTS ---
        self.cur.execute("DELETE FROM patients")
        p_names = [
            "Aarav", "Ishita", "Vihaan", "Ananya", "Sai", "Kabir", "Zara", "Rohan", "Meera", "Arjun",
            "Diya", "Aditya", "Sanya", "Ishaan", "Kiara", "Karan", "Riya", "Aaryan", "Isha", "Rahul",
            "Priya", "Suresh", "Sneha", "Amit", "Deepa", "Vijay", "Lata", "Ravi", "Monica", "Sanjay",
            "Alia", "Varun", "Ranbir", "Sid", "Pooja", "Prabhas", "Shraddha", "Tiger", "Kriti", "Vicky",
            "Sara", "Kartik", "Janhvi", "Ananya", "Dev", "Tara", "Neil", "Avni", "Reyansh", "Myra"
        ]
        surnames = ["Sharma", "Patel", "Gupta", "Iyer", "Kumar", "Singh", "Reddy", "Kapoor", "Verma", "Malhotra"]
        diseases = ["Fever", "Migraine", "Fracture", "Asthma", "Diabetes", "Hypertension", "Infection", "Checkup"]
        statuses = ["Stable", "Recovering", "Observation", "Critical", "Discharged"]
        
        full_p_data = []
        for i in range(50):
            pid = f"P-{100 + i}"
            name = f"{random.choice(p_names)} {random.choice(surnames)}"
            doc = random.choice(doctors_list)[1]
            full_p_data.append((pid, name, "2026-03-04", doc, random.choice(diseases), random.choice(statuses), f"R-{random.randint(100,500)}", random.randint(1000, 25000)))
        
        self.cur.executemany("INSERT INTO patients VALUES (?,?,?,?,?,?,?,?)", full_p_data)
        self.conn.commit()

    def setup_ui_skeleton(self):
        self.navbar = ctk.CTkFrame(self, height=80, fg_color="#1E293B", corner_radius=0)
        ctk.CTkLabel(self.navbar, text="✚ HOSPITAL MANAGEMENT", font=("Inter", 26, "bold"), text_color="#3B82F6").pack(side="left", padx=40)
        self.nav_btn_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        self.nav_btn_frame.pack(side="left", expand=True)
        self.main_area = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)

    # --- Authentication ---
    def show_login_screen(self):
        self.auth_container = ctk.CTkFrame(self, fg_color="#0F172A")
        self.auth_container.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.auth_frame = ctk.CTkFrame(self.auth_container, fg_color="#1E293B", corner_radius=20, width=450, height=500)
        self.auth_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.render_login_widgets()

    def render_login_widgets(self):
        for w in self.auth_frame.winfo_children(): w.destroy()
        ctk.CTkLabel(self.auth_frame, text="Sign In", font=("Inter", 32, "bold")).pack(pady=(50, 30))
        self.u_ent = ctk.CTkEntry(self.auth_frame, placeholder_text="Username", width=300, height=45)
        self.u_ent.pack(pady=10)
        self.p_ent = ctk.CTkEntry(self.auth_frame, placeholder_text="Password", show="*", width=300, height=45)
        self.p_ent.pack(pady=10)
        ctk.CTkButton(self.auth_frame, text="LOGIN", command=self.handle_login, width=300, height=45).pack(pady=20)
        ctk.CTkButton(self.auth_frame, text="Create Account", fg_color="transparent", command=self.render_signup_widgets).pack()

    def render_signup_widgets(self):
        for w in self.auth_frame.winfo_children(): w.destroy()
        ctk.CTkLabel(self.auth_frame, text="Create Account", font=("Inter", 32, "bold")).pack(pady=(50, 30))
        self.nu_ent = ctk.CTkEntry(self.auth_frame, placeholder_text="New Username", width=300, height=45)
        self.nu_ent.pack(pady=10)
        self.np_ent = ctk.CTkEntry(self.auth_frame, placeholder_text="New Password", show="*", width=300, height=45)
        self.np_ent.pack(pady=10)
        ctk.CTkButton(self.auth_frame, text="REGISTER", command=self.handle_signup, width=300, height=45).pack(pady=20)
        ctk.CTkButton(self.auth_frame, text="Back to Login", fg_color="transparent", command=self.render_login_widgets).pack()

    def handle_signup(self):
        u, p = self.nu_ent.get(), self.np_ent.get()
        if u and p:
            try:
                self.cur.execute("INSERT INTO users VALUES (?,?)", (u, p))
                self.conn.commit(); messagebox.showinfo("Success", "Account Created!"); self.render_login_widgets()
            except: messagebox.showerror("Error", "Username exists")
        else: messagebox.showerror("Error", "Empty Fields")

    def handle_login(self):
        self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (self.u_ent.get(), self.p_ent.get()))
        if self.cur.fetchone():
            self.auth_container.destroy()
            self.navbar.pack(side="top", fill="x")
            self.main_area.pack(side="bottom", fill="both", expand=True, padx=40, pady=20)
            self.build_nav(); self.show_dashboard()
        else: messagebox.showerror("Error", "Invalid Login")

    def build_nav(self):
        for w in self.nav_btn_frame.winfo_children(): w.destroy()
        menus = [("📊 Dashboard", self.show_dashboard), ("👥 Patients", self.show_patients), 
                 ("👨‍⚕️ Doctors", self.show_doctors), ("🏥 Staff", self.show_staff), ("📄 Reports", self.show_reports)]
        for text, cmd in menus:
            ctk.CTkButton(self.nav_btn_frame, text=text, command=cmd, width=130, fg_color="transparent", font=("Inter", 13, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(self.navbar, text="Logout", width=80, fg_color="#EF4444", command=self.logout).pack(side="right", padx=40)

    def show_dashboard(self):
        self.clear_area()
        ctk.CTkLabel(self.main_area, text="Hospital Analytics", font=("Inter", 32, "bold")).pack(anchor="w", pady=10)
        self.cur.execute("SELECT COUNT(*), SUM(bill) FROM patients")
        p_count, revenue = self.cur.fetchone()
        revenue = revenue if revenue else 0
        container = ctk.CTkFrame(self.main_area, fg_color="transparent")
        container.pack(fill="x", pady=20)
        self.create_stat_card(container, "Total Patients", str(p_count), "#3B82F6")
        self.create_stat_card(container, "Net Revenue", f"₹{revenue:,.2f}", "#10B981")
        self.cur.execute("SELECT COUNT(*) FROM staff")
        self.create_stat_card(container, "Hospital Personnel", f"{self.cur.fetchone()[0]} Members", "#F59E0B")

    def create_stat_card(self, parent, title, val, color):
        card = ctk.CTkFrame(parent, fg_color="#1E293B", width=380, height=180, corner_radius=15)
        card.pack(side="left", padx=15); card.pack_propagate(False)
        ctk.CTkLabel(card, text=val, font=("Inter", 40, "bold"), text_color=color).pack(pady=(50,0))
        ctk.CTkLabel(card, text=title, font=("Inter", 16)).pack()

    def show_patients(self, filter_text=""):
        self.clear_area()
        top_f = ctk.CTkFrame(self.main_area, fg_color="transparent")
        top_f.pack(fill="x", pady=10)
        self.add_search_bar_to_frame(top_f, "Search Patient ID/Name...", self.show_patients)
        
        header_row = ctk.CTkFrame(self.main_area, fg_color="#334155", height=40)
        header_row.pack(fill="x", pady=(10, 5))
        headers = [("ID", 80), ("Patient Name", 200), ("Check-in", 120), ("Doctor", 180), ("Status", 120), ("Room", 80)]
        for text, width in headers:
            ctk.CTkLabel(header_row, text=text, width=width, font=("Inter", 12, "bold")).pack(side="left", padx=5)

        self.cur.execute("SELECT * FROM patients WHERE pid LIKE ? OR name LIKE ?", (f'%{filter_text}%', f'%{filter_text}%'))
        for p in self.cur.fetchall():
            row = ctk.CTkFrame(self.main_area, fg_color="#1E293B", height=60, corner_radius=8)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=p[0], width=80).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=p[1], width=200, font=("Inter", 13, "bold"), anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=p[2], width=120).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=p[3], width=180, text_color="#60A5FA").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=p[5], width=120).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=p[6], width=80).pack(side="left", padx=5)
            ctk.CTkButton(row, text="Update", width=60, command=lambda x=p: self.patient_form(x)).pack(side="right", padx=5)
            ctk.CTkButton(row, text="Delete", width=60, fg_color="#EF4444", command=lambda x=p[0]: self.delete_patient(x)).pack(side="right", padx=10)

    def show_doctors(self, filter_text=""):
        self.clear_area()
        self.add_search_bar("Search Doctors...", self.show_doctors)
        self.cur.execute("SELECT * FROM staff WHERE role='Doctor' AND (name LIKE ? OR specialty LIKE ?)", (f'%{filter_text}%', f'%{filter_text}%'))
        for d in self.cur.fetchall():
            card = ctk.CTkFrame(self.main_area, fg_color="#1E293B", height=80)
            card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text="●", text_color="#10B981", font=("Inter", 20)).pack(side="left", padx=20)
            ctk.CTkLabel(card, text=f"{d[1]} - {d[3]}", font=("Inter", 18, "bold")).pack(side="left")

    def show_staff(self, filter_text=""):
        self.clear_area()
        self.add_search_bar("Search Staff...", self.show_staff)
        self.cur.execute("SELECT * FROM staff WHERE role!='Doctor' AND (name LIKE ? OR role LIKE ?)", (f'%{filter_text}%', f'%{filter_text}%'))
        for s in self.cur.fetchall():
            row = ctk.CTkFrame(self.main_area, fg_color="#1E293B", height=60, corner_radius=10)
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=f"{s[2]}", width=150, text_color="#3B82F6", font=("Inter", 12, "bold")).pack(side="left", padx=10) 
            ctk.CTkLabel(row, text=f"{s[1]}", font=("Inter", 15, "bold")).pack(side="left") 
            ctk.CTkLabel(row, text=f"ID: {s[0]}", text_color="#94A3B8").pack(side="right", padx=20)

    # --- ADVANCED LONG REPORT LOGIC ---
    def show_reports(self):
        self.clear_area()
        ctk.CTkLabel(self.main_area, text="Clinical Documentation Center", font=("Inter", 32, "bold")).pack(pady=20)
        self.report_box = ctk.CTkFrame(self.main_area, fg_color="#1E293B", height=350, width=600, corner_radius=20)
        self.report_box.pack(pady=20); self.report_box.pack_propagate(False)
        self.rep_ent = ctk.CTkEntry(self.report_box, placeholder_text="Enter Patient ID (e.g. P-101)", width=400, height=50)
        self.rep_ent.pack(pady=40)
        
        btn_f = ctk.CTkFrame(self.report_box, fg_color="transparent")
        btn_f.pack()
        ctk.CTkButton(btn_f, text="GENERATE PDF", command=lambda: self.download_report_logic(False), fg_color="#3B82F6", height=45).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="VIEW REPORT", command=lambda: self.download_report_logic(True), fg_color="#10B981", height=45).pack(side="left", padx=10)

    def download_report_logic(self, open_file=False):
        pid_in = self.rep_ent.get().strip().upper()
        self.cur.execute("SELECT * FROM patients WHERE UPPER(pid)=?", (pid_in,))
        p = self.cur.fetchone()
        if p:
            fn = f"Detailed_Medical_Record_{p[0]}.pdf"
            c = canvas.Canvas(fn, pagesize=A4)
            width, height = A4
            
            # Header
            c.setStrokeColor(colors.blue)
            c.rect(40, height - 80, width - 80, 60, fill=0)
            c.setFont("Helvetica-Bold", 20); c.drawCentredString(width/2, height - 55, "HOSPITAL CLINICAL SUMMARY")
            c.setFont("Helvetica", 10); c.drawCentredString(width/2, height - 70, "123 Healthcare Blvd, Medical District, India")
            
            # Patient Info Section
            y = height - 120
            c.setFont("Helvetica-Bold", 14); c.drawString(50, y, "Patient Information"); y -= 25
            c.setFont("Helvetica", 12)
            info = [f"Patient ID: {p[0]}", f"Full Name: {p[1]}", f"Check-in Date: {p[2]}", f"Assigned Doctor: {p[3]}", f"Room/Ward: {p[6]}"]
            for line in info:
                c.drawString(60, y, line); y -= 20
            
            # Vitals Section (Dummy Data for Length)
            y -= 20
            c.setFont("Helvetica-Bold", 14); c.drawString(50, y, "Clinical Vitals"); y -= 25
            c.setFont("Helvetica", 11)
            vitals = [f"Blood Pressure: {random.randint(110,140)}/{random.randint(70,90)} mmHg", 
                      f"Heart Rate: {random.randint(65,95)} bpm", 
                      f"Oxygen Saturation (SpO2): {random.randint(95,100)}%", 
                      f"Temperature: {random.uniform(97.5, 101.5):.1f} °F"]
            for v in vitals:
                c.drawString(60, y, v); y -= 20

            # Diagnosis Section
            y -= 20
            c.setFont("Helvetica-Bold", 14); c.drawString(50, y, "Diagnosis & Progress"); y -= 25
            c.setFont("Helvetica", 11)
            c.drawString(60, y, f"Primary Diagnosis: {p[4]}")
            y -= 20
            c.drawString(60, y, f"Current Status: {p[5]}")
            y -= 30
            
            # Notes Section (Longer Text)
            c.setFont("Helvetica-Bold", 14); c.drawString(50, y, "Doctor's Clinical Notes"); y -= 25
            c.setFont("Helvetica-Oblique", 10)
            long_note = [
                "The patient presented with symptoms consistent with the primary diagnosis.",
                "Observations indicate steady improvement under current medication protocols.",
                "Recommend continued monitoring of vitals and physical therapy sessions.",
                "Patient is advised to maintain a strict dietary regimen as discussed.",
                "Follow-up appointment is required in 14 days for reassessment."
            ]
            for note in long_note:
                c.drawString(60, y, f"- {note}"); y -= 18

            # Billing
            y -= 30
            c.setFont("Helvetica-Bold", 12); c.drawString(50, y, f"Total Outstanding Bill: INR {p[7]:,.2f}")
            
            # Footer / Signature
            c.line(50, 100, 200, 100)
            c.setFont("Helvetica", 10); c.drawString(50, 85, "Authorized Medical Officer")
            c.drawRightString(width - 50, 85, f"Date generated: 2026-03-04")

            c.save()
            if open_file: os.startfile(fn)
            else: messagebox.showinfo("Success", f"Report saved as {fn}")
        else: messagebox.showerror("Error", "ID Not Found")

    # --- Utilities ---
    def add_search_bar(self, placeholder, callback):
        f = ctk.CTkFrame(self.main_area, fg_color="transparent")
        f.pack(fill="x", pady=10)
        self.add_search_bar_to_frame(f, placeholder, callback)

    def add_search_bar_to_frame(self, frame, placeholder, callback):
        e = ctk.CTkEntry(frame, placeholder_text=placeholder, width=400, height=40)
        e.pack(side="left")
        ctk.CTkButton(frame, text="Search", width=100, command=lambda: callback(e.get())).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Reset", fg_color="#475569", width=80, command=lambda: callback("")).pack(side="left")

    def patient_form(self, edit_data=None):
        win = ctk.CTkToplevel(self); win.geometry("500x700"); win.attributes("-topmost", True)
        labels = ["ID", "Name", "Date", "Doctor", "Disease", "Status", "Room", "Bill"]
        ents = {}
        for i, l in enumerate(labels):
            ctk.CTkLabel(win, text=l).pack(pady=(10,0))
            e = ctk.CTkEntry(win, width=350); e.pack(pady=2)
            if edit_data: e.insert(0, edit_data[i])
            ents[l] = e
        def save():
            v = [ents[l].get() for l in labels]
            if edit_data: self.cur.execute("UPDATE patients SET name=?, date_in=?, doctor=?, disease=?, status=?, room=?, bill=? WHERE pid=?", (v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[0]))
            else: self.cur.execute("INSERT INTO patients VALUES (?,?,?,?,?,?,?,?)", v)
            self.conn.commit(); win.destroy(); self.show_patients()
        ctk.CTkButton(win, text="SAVE", fg_color="#3B82F6", command=save).pack(pady=30)

    def delete_patient(self, pid):
        if messagebox.askyesno("Confirm", "Delete record?"):
            self.cur.execute("DELETE FROM patients WHERE pid=?", (pid,)); self.conn.commit(); self.show_patients()

    def clear_area(self):
        for w in self.main_area.winfo_children(): w.destroy()
    def logout(self):
        python = os.sys.executable; os.execl(python, python, *os.sys.argv)
    def on_closing(self):
        self.conn.close(); self.destroy()

if __name__ == "__main__":
    app = HospitaKrEnterprise()
    app.mainloop()