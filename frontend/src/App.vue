<script setup>
import HelloWorld from "./components/HelloWorld.vue";
import LoginForm from "./components/LoginForm.vue";
import axios from 'axios';
</script>

<template>
  <header>
    <img
      alt="Vue logo"
      class="logo"
      src="./assets/dog.webp"
      width="125"
      height="125"
    />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <main>
    <LoginForm/>
    <button @click="getResponseData" class="submit">submit</button>
    <div v-if="isVisible" class = "box">{{responseData}}</div>
  </main>

</template>

<script>
export default {
  data() {
    return {
      isVisible: true,
      username: "okk",
      responseData: ''
    }
  },
  methods: {
    toggleBox(){
      this.isVisible = !this.isVisible
    },
    getResponseData(){
      axios.get('http://127.0.0.1:5000/api/recommend/query/First Post').then((response)=>{
        console.log(response.data);
        this.responseData=response.data;
      }).catch((response)=>{
        console.log(response);
      })
    }
  }
}
</script>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.box {
  background-color: rgb(171, 141, 198);
  height: 200px;
  width: 200px;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }


}
</style>
