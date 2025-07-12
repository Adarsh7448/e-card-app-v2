<template>
    <form @submit.prevent="requestCard">
        <div class="mb-3">
            <label for="Input1" class="form-label">Fullname</label>
            <input type="text" class="form-control" id="Input1" v-model="formData.fullname">
        </div>
        <div class="mb-3">
            <label for="Input2" class="form-label">DOB</label>
            <input type="text" class="form-control" id="Input2" v-model="formData.dob" >
        </div>
        <div class="mb-3">
            <label for="Input3" class="form-label">Ph no.</label>
            <input type="text" class="form-control" id="Input3" v-model="formData.ph" >
        </div>
        <div style="text-align: center;">
        <input type="submit" class="btn btn-primary" value="Request"> <br>
        <!-- <button @click="" class="btn btn-primary">Login</button> <br> -->
        </div>
    </form>
</template>

<script>
import axios from 'axios';
export default {
    data(){
        return {
            formData: {
                fullname: "",
                dob: "",
                ph: ""
            }
        }
    },
    methods: {
        requestCard: function() {
            const cardname = this.$route.params.cardname;
            const response = axios.post(`http://127.0.0.1:5000/api/request/${cardname}`, JSON.stringify(this.formData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    console.log(res)
            }).catch(err => this.error = err.response.data.message)

        }
    }
}
</script>