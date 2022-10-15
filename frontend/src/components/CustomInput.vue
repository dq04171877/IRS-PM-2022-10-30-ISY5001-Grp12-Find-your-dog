<script setup>
  defineProps({
      label: {
        type: String,
        required: true,
    },
      modelValue:{
        type: String,
        required: true,
      }
  });
</script>

<template>
  <label>
    {{ label }}
    <input type = "text" v-model="inputValue"/>
  </label>
</template>

<script>
  export default {
    props: ['label', 'modelValue'],
    computed: {
      inputValue:{
        get() {
          return this.modelValue
        },
        set(value) {
          console.log(value)
          this.$emit('update:modelValue')
        }
      }
    }
    // data() {
    //     return {
    //         inputValue: ''
    //     }
    // }
  }

</script>

<style scoped>
  input{
    margin: 10px;
    display: block;
  }
</style>