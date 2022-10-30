<script setup>
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <h1>{{title}}</h1>
    <input type ="email" v-model="email"/>
    <input type ="password" v-model="password"/>
    <CustomInput  v-model="hdbValue" :label="hdbLabel"/>
    <CustomInput  v-model="genderValue" :label="genderLabel"/>
    <button>Log in</button>
  </form>
  
</template>

<script>
import CustomInput from './CustomInput.vue';
  export default {
    data() {
        return {
            title: "Login Form",
            email: "",
            password: "",
            hdbLabel: "hdb",
            genderLabel: 'gender',
            hdbValue: 'sgsd',
            genderValue: '45645rt'
        };
    },
    methods: {
        handleSubmit() {
            console.log(this.email, this.password);
        }
    },
    components: { CustomInput }
};
</script>

<style scoped>
  input{
    margin: 10px;
    display: block;
  }
</style>

  