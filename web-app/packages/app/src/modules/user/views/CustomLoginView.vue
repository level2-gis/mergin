<template>
  <login-view-template @userLogin="handleUserLogin">
    <template #aside>
      <div class="custom-aside">
        <h2>MerginMaps in GEO-PORTAL</h2>
        <p>Ponujamo gostovanje podatkov zajetih z aplikacijo MerginMaps v Sloveniji. Podatki se lahko tudi sinhronizirajo z vašo PostgreSQL bazo in delijo preko GEO-PORTAL-a.</p>
        <br>
        <p>Za več informacij nas <a class="text-color-forest" href="https://level2.si/contact/?podrocje=merginmaps" target="_blank"><b>kontaktirajte</b></a>.</p>
	<br><p>Kaj je <a class="text-color-forest" href="https://site.geo-portal.si/" target="_blank"><b>GEO-PORTAL</b></a>?</p>
	<img src="/level2.svg" alt="level2" />
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  padding: 2rem;
}

.custom-aside img {
  max-width: 100px;
  height: auto;
  margin-top: 5rem;
}
</style>
