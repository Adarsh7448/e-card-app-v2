<script>
import axios from 'axios'
export default {
    data(){
        return {
           formData:{
            username: "",
            password: ""
           },
           token: "" 
        }
    },
    methods:{
        loginUser(){
            // event.preventDefault()
            // console.log(`Username: ${this.formData.username}, Password: ${this.formData.password}`)
            const response = axios.post("http://127.0.0.1:5000/api/login", JSON.stringify(this.formData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            })
            response
            .then(res => {
                if(res.status == 200){
                    this.token = res.data.access_token
                    localStorage.setItem("token", res.data.access_token)
                }
                else{
                    console.log(res.response.data)
                }
            })
            // .then(data => console.log(data))
        },
        logoutUser(){
            localStorage.clear()
        }
    }
}
</script>

<template>
    <div id="main">
        <div id="canvas">
            <div id="form-body">
                <h1>Login Form</h1>
                <form @submit.prevent="loginUser">
                <div class="mb-3">
                    <label for="Input1" class="form-label">Username</label>
                    <input type="text" class="form-control" id="Input1" v-model="formData.username">
                </div>
                <div class="mb-3">
                    <label for="Input2" class="form-label">Password</label>
                    <input type="password" class="form-control" id="Input2" v-model="formData.password" >
                </div>
                <div style="text-align: center;">
                <input type="submit" class="btn btn-primary" value="Login"> <br>
                <!-- <button @click="" class="btn btn-primary">Login</button> <br> -->
                Are you a new user? <a href="/register">Register</a>
               </div>
               </form>
               <button @click="logoutUser" class="btn btn-danger">Logout</button>
            </div>
        </div>
    </div>
</template>


<style>
    #form-body{
        height: 337px;
    }
</style>