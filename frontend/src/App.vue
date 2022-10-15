<script setup>
import HelloWorld from "./components/HelloWorld.vue";
import LoginForm from "./components/LoginForm.vue";
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
    <button @click="toggleBox" class="submit">{{isVisible}}</button>
    <div v-if="isVisible" class = "box"></div>
  </main>

</template>

<script>
export default {
  data() {
    return {
      isVisible: true,
      username: "okk"
    }
  },
  methods: {
    toggleBox(){
      this.isVisible = !this.isVisible
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
  background-color: blueviolet;
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

  input{
    margin: 10px;
    display: block;
  }
}
</style>
