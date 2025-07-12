<script>
export default {
    methods: {
        logoutUser(){
            localStorage.clear();
            this.$router.push('/')
        }
    }
}
</script>

<template>
    <nav class="navbar bg-primary-subtle">
        <div class="container-fluid">   
            <RouterLink class="navbar-brand" to="/dashboard">E-Card App</RouterLink>
            <button @click="logoutUser" class="btn btn-danger">Logout</button>
        </div>
    </nav>
</template>

<style>
</style>