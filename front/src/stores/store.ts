import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({ 
      avatar: "",
      name:"" ,
      notLogin:false,
    }),
    getters: {
    },
    actions: {
    },
  })