<template>
    <div v-if="token">
        <div v-if="role == 'user'">
            <h1>This is user, {{ userData.username }}</h1>
            <table>
                <thead>
                    <tr>
                        <th>Card Name</th>
                        <th>User</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="card in userData.available_cards" :key="card.cardname">
                        <td>{{ card.cardname }}</td>
                        <td>{{ userData.username }}</td>
                        <td>
                            <RouterLink to="">
                                <button class="btn btn-primary">View</button>
                            </RouterLink>                            
                        </td>
                    </tr>
                </tbody>
            </table>
            <table>
                <thead>
                    <tr>
                        <th>Card Name</th>
                        <th>User</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="card in userData.card_requests" :key="card.cardname">
                        <td>{{ card.cardname }}</td>
                        <td>{{ userData.username }}</td>
                        <td>{{ card.status }}</td>
                    </tr>
                </tbody>
            </table>
            <div>
                <RouterLink to="/user/request/aadhar">
                    <button class="btn btn-warning">Request Aadhar</button>
                </RouterLink>
                <RouterLink to="/user/request/voter">
                    <button class="btn btn-warning">Request Voter</button>
                </RouterLink>
                <RouterLink to="/user/request/pan">
                    <button class="btn btn-warning">Request PAN</button>
                </RouterLink>
                <RouterLink to="/user/request/driving">
                    <button class="btn btn-warning">Request Driving</button>
                </RouterLink>
                
            </div>
        </div>
        <div v-else>
            <h1>This is admin</h1>
        </div>
    </div>
    <div v-else>
        <h1>Please login</h1> 
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data(){
        return {
            token: "",
            role: "",
            userData: ""
        }
    },
    mounted(){
        this.loadToken()
        this.loadUser()
    },
    methods: {
        loadToken: function() {
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
        },
        loadUser: function() {

            const response = axios.get("http://127.0.0.1:5000/api/dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${this.token}` 
                }
            })
            response
            .then(res => {
                   this.role = res.data.role;
                   this.userData = res.data
            }).catch(err => this.error = err.response.data.message)

        }
    }
}
</script>

