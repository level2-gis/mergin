<template>
  <login-view-template @userLogin="handleUserLogin">
    <template #aside>
      <div class="custom-aside">
        <h2>Welcome to My Platform</h2>
        <p>Geospatial collaboration made easy.</p>
        <img src="@/assets/custom-side-image.svg" alt="Custom side" />
      </div>
    </template>
  </login-view-template>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { LoginViewTemplate, useUserStore } from '@mergin/lib'
import { mapActions } from 'pinia'

export default defineComponent({
  name: 'LoginView',
  components: { LoginViewTemplate },
  methods: {
    ...mapActions(useUserStore, [
      'userLogin',
      'redirectAfterLogin',
      'redirectFromLoginAfterLogin'
    ]),
    async handleUserLogin(payload) {
      try {
        await this.userLogin(payload)
        if (payload.currentRoute.query.redirect) {
          await this.redirectAfterLogin({ currentRoute: payload.currentRoute })
        } else {
          await this.redirectFromLoginAfterLogin({ currentRoute: payload.currentRoute })
        }
      } catch (err) {
        console.error(err)
      }
    }
  }
})
</script>

<style scoped>
.custom-aside {
  text-align: center;
  padding: 2rem;
  color: #333;
}

.custom-aside img {
  max-width: 100%;
  height: auto;
  margin-top: 1rem;
}
</style>
