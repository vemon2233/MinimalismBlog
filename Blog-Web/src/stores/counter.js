export const useCounterStore = defineStore('counter', {
  state() {
    return {
      num: 100
    }
  },
  actions: {
    increase() {
      this.num ++
    }
  }
})