import { createWebHistory, createRouter } from "vue-router";
import Content from "./components/Content.vue";
import LoginPage from "./components/LoginPage.vue";
// import RegisterPage from "./components/RegisterPage.vue"
import Dashboard from "./components/Dashboard.vue";
import RequestCard from "./components/RequestCard.vue";

const routes = [
    { path: "/", component: Content},
    { path: "/login", component: LoginPage},
    // { path: "/register", component: RegisterPage},
    { path: "/dashboard", component: Dashboard},
    // { path: "/user", components: [
    //     // { path: "", component: User},
    //     { path: "request/:cardname", component: RequestCard},
    //     // { path: "view/:cardname", component: ViewCard}
    //     ],
    // }  
    { path: "/user/request/:cardname", component: RequestCard}  
]

export const router = createRouter({
    history: createWebHistory(),
    routes // --> routes: routes
})


