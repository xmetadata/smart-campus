<template>
  <div>
    <div class="vux-demo">
      <img class="logo" src="../assets/vux_logo.png">
      <h1> </h1>
    </div>
    <group title="cell demo">
      <cell title="VUX" value="cool" is-link></cell>
      <x-input title="title" v-model="xi"></x-input>
      <x-number title="title" v-model="xn"></x-number>
    </group>
  </div>
</template>

<script>
import { Group, Cell, XInput, XNumber } from 'vux'

export default {
  components: {
    Group,
    Cell,
    XInput,
    XNumber
  },
  data () {
    return {
      // note: changing this line won't causes changes
      // with hot-reload because the reloaded component
      // preserves its current state and we are modifying
      // its initial state.
      msg: 'Hello World!',
      xi: '',
      xn: 0
    }
  }
}
</script>

<style>
.vux-demo {
  text-align: center;
}
.logo {
  width: 100px;
  height: 100px
}
</style>
