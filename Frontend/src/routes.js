import { createWebHistory, createRouter } from "vue-router";
import Content from "./components/Content.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import AddDoctor from "./components/AddDoctor.vue";
import PatientHistory from "./components/PatientHistory.vue";
import AddDepartment from "./components/AddDepartment.vue";
import AdminWelcome from "./components/AdminWelcome.vue";
import EditDoctor from "./components/EditDoctor.vue";
import EditDepartment from "./components/EditDepartment.vue";

const routes = [
    { path: "/", component: Content },
    { path: "/login", component: LoginPage },
    { path: "/register", component: RegisterPage },
    { path: "/admin_welcome", component: AdminWelcome },
    { path: "/admin_dashboard", component: AdminDashboard },
    { path: "/add_doctor", component: AddDoctor },
    { path: "/patient_history", component: PatientHistory },
    { path: "/add_department", component: AddDepartment },
    { path: "/edit_doctor/:id", component: EditDoctor },
    { path: "/edit_department/:id", component: EditDepartment },
]

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL || '/'),
    routes,
});