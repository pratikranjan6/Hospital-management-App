import { createWebHistory, createRouter } from "vue-router";
import Content from "./components/Content.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import AddDoctor from "./components/AddDoctor.vue";
import PatientHistory from "./components/PatientHistory.vue";
import DoctorPaHistory from "./components/DoctorPaHistory.vue";
import AddDepartment from "./components/AddDepartment.vue";
import AdminWelcome from "./components/AdminWelcome.vue";
import EditDoctor from "./components/EditDoctor.vue";
import EditDepartment from "./components/EditDepartment.vue";
import DoctorDashboard from "./components/DoctorDashboard.vue";
import UserDashboard from "./components/UserDashboard.vue";
import DepartmentInfo from "./components/DepartmentInfo.vue";
import EditProfile from "./components/EditProfile.vue";
import History from "./components/History.vue";
import DoctorAvailability from "./components/DoctorAvailability.vue";
import BookAppointment from "./components/BookAppointment.vue";
import EditPatient from "./components/EditPatient.vue";

const routes = [
    { path: "/", component: Content },
    { path: "/login", component: LoginPage },
    { path: "/register", component: RegisterPage },
    { path: "/admin_welcome", component: AdminWelcome },
    { path: "/admin_dashboard", component: AdminDashboard },
    { path: "/add_doctor", component: AddDoctor },
    { path: "/patient_history", component: PatientHistory },
    { path: "/doctor_patient_history", component: DoctorPaHistory },
    { path: "/add_department", component: AddDepartment },
    { path: "/edit_doctor/:id", component: EditDoctor },
    { path: "/edit_department/:id", component: EditDepartment },
    { path: "/doctor_dashboard", component: DoctorDashboard },
    { path: "/doctor_availability", component: DoctorAvailability },
    { path: "/user_dashboard", component: UserDashboard },
    { path: "/department/:id", component: DepartmentInfo },
    { path: "/book-appointment/:doctorId", name: "bookAppointment", component: BookAppointment },
    { path: "/edit-patient/:appointmentId", name: "editPatient", component: EditPatient },
    { path: "/edit-profile", component: EditProfile },
    { path: "/history", component: History },
]

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL || '/'),
    routes,
});