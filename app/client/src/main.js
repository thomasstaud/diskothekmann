import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createStore } from 'vuex'

import { createRouter, createWebHistory } from 'vue-router'

import Home from './views/Home.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'home', component: Home },
    ],
    scrollBehavior(to, from, savedPosition) {
      // always scroll to top
      return { top: 0 }
    },
});

const store = createStore({
    state () {
      return {
        currentTrack: null,
        currentPlaylist: null,
      }
    },
    mutations: {
      set_track (state, track) {
        state.currentPlaylist = null;
        state.currentTrack = track;
      },
      set_playlist (state, playlist) {
        state.currentTrack = null;
        state.currentPlaylist = playlist;
      }
    }
  })

const app = createApp(App)
app.use(router);
app.use(store);
app.mount('#app');
