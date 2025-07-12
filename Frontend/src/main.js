import { createApp } from 'vue'
// import './style.css'
import './myStyle.css'
import App from './App.vue'
import { router } from "./routes.js"

createApp(App).use(router).mount("#app")
