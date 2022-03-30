# Copyright (C) 2021 Lutra Consulting Limited. All rights reserved.
# Do not distribute without the express permission of the author.

<template>
  <page-view :style="`padding-left: ${drawer ? 280 : 20}px; overflow-y: auto; padding-right:20px; margin-right: 0px;`">
    <v-layout class="column fill-height main-content">
      <v-container>
          <v-row >
            <v-card v-if="!app.user.verified_email"
                    outlined
                    class="bubble mt-3"
                    style="background-color: orange; color: rgba(0,0,0,.87);">
              Tvoja e-pošta še ni potrjena
              <v-btn color="#ecf3ff"
                     @click="sendConfirmationEmail(app.user.email)"
                     style="float:right;"
              >Pošlji potrditveno sporočilo
              </v-btn>
            </v-card>
          </v-row>
          <v-row v-if="usage > 90"
                 >
            <v-card
                class="bubble mt-3"
                style="background-color: orange; color: rgba(0,0,0,.87);"
                outlined
            >
              <span> Your storage is almost full ({{usage}}%). Soon you will not able to sync your projects.</span>
            </v-card>
          </v-row>
          <v-row >
            <v-card
                class="bubble mt-3"
                outlined>
              <h3>Namesti si aplikacijo</h3>
              <p>Z aplikacijo Input enostavno zajameš prostorske podatke prek mobilnega telefona/tablice.</p>
              <v-row>
                <v-col cols="6"
                       md="3"
                       sm="3"
                >
                  <a href='https://geo-portal.si/uploads/input_level2_130.apk'>
                    Android
                  </a>
                </v-col>
                <v-col cols="7"
                       md="3"
                       sm="3"
                >
                  <div class="app-store-button">
                    <a href='https://apps.apple.com/us/app/input/id1478603559?ls=1' target="_blank">
                      <img alt='Get it on Apple store' src="../assets/App_Store.svg" width="138px"
                      />
                    </a>
                  </div>
                </v-col>
              </v-row>
            </v-card>
          </v-row>
        <v-row v-if="transfers && transfers.length > 0">
            <v-card class="bubble mt-3">
              <h3>Project transfers</h3>
              <v-card-text>
                <transfers-table :namespace="app.user.username"/>
              </v-card-text>
            </v-card>
          </v-row>
          <v-row v-if="accessRequests && accessRequests.length > 0">
            <v-card class="bubble mt-3">
              <h3>Zahteve za prenos projektov</h3>
              <v-card-text>
                <project-access-request-table/>
              </v-card-text>
            </v-card>
          </v-row>
          <v-row>
            <v-card class="bubble mt-3"
            :outlined="true"
            color="white">
              <h3>Nedavni aktivni projekti</h3>
              <v-card-text style="padding-left: 0px">
                <projects-table
                    :show-namespace="true"
                    :showFooter="false"
                    :showHeader="false"
                    :sortable="false"
                    :public="false"
                    :initialOptions="{
              sortBy: ['updated'],
              sortDesc: [true],
              itemsPerPage: 5,
              page: 1
            }"
                    show-tags
                />
              </v-card-text>
            </v-card>
          </v-row>
        </v-container>
    </v-layout>
  </page-view>
</template>

<script>
import MerginAPI from '../mixins/MerginAPI'
import { mapState } from 'vuex'
import PageView from '@/views/PageView'
import OrganisationForm from '@/organisation/components/OrganisationForm'
import ProjectForm from '@/components/ProjectForm'
import OrganisationsMixin from '@/mixins/Organisation'
import ProjectsTable from '@/components/ProjectsTable'
import ProjectAccessRequestTable from '@/components/ProjectAccessRequestTable'
import TransfersTable from '@/components/TransfersTable'


export default {
  mixins: [MerginAPI, OrganisationsMixin],
  name: 'dashboard',
  components: { PageView, ProjectsTable, ProjectAccessRequestTable, TransfersTable },
  computed: {
    ...mapState(['app', 'drawer', 'transfers', 'accessRequests']),
    userProfile () {
      return this.app.user.profile
    },
    usage () {
      return Math.floor((this.userProfile.disk_usage / this.userProfile.storage) * 100)
    }
  },
  created () {
    this.fetchAccessRequests()
    this.fetchTransfers(this.app.user.username)
  },
  methods: {
    newOrganisationDialog () {
      const props = { organisation: {} }
      const dialog = { maxWidth: 500, persistent: true }
      const listeners = {
        success: () => {
          this.getUserOrganisations()
          this.$router.push({ name: 'user_organisations', params: { username: this.app.user.username } })
        }
      }
      this.$dialog.show(OrganisationForm, { props, listeners, dialog })
    },
    newProjectDialog () {
      const dialog = { maxWidth: 500, persistent: true }
      this.$dialog.show(ProjectForm, { dialog })
    }
  }
}
</script>

<style scoped lang="scss">
  .sidebar {
    height: 100vh;
    background-color: #4caf50;
    top: 0px;
    max-height: calc(100% + 0px);
    transform: translateX(0%);
    width: 260px;
  }

  .v-navigation-drawer {
    -webkit-overflow-scrolling: touch;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-direction: column;
    flex-direction: column;
    left: 0;
    max-width: 100%;
    overflow: hidden;
    pointer-events: auto;
    top: 0;
    -webkit-transition-duration: .2s;
    transition-duration: .2s;
    -webkit-transition-timing-function: cubic-bezier(.4, 0, .2, 1);
    transition-timing-function: cubic-bezier(.4, 0, .2, 1);
    will-change: transform;
    -webkit-transition-property: width, -webkit-transform;
    transition-property: width, -webkit-transform;
    transition-property: transform, width;
    transition-property: transform, width, -webkit-transform;
  }

  .bubble {
    width: 800px;
    background-color: #eaebef;
    padding: 20px 25px 15px 15px;
  }

  .app-store-button {
      padding-top: 12px;
    }

  @media only screen and (max-width: 599px) {
    .app-store-button {
      padding-left: 12px;
      padding-top: 0px;
    }
  }

  @media only screen and (min-width: 600px) and (max-width: 960px) {
    .app-store-button {
      margin-left: 20%;
    }
  }

  h3 {
    color: #2d4470;
  }
</style>
