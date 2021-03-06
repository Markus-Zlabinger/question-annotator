import Vue from 'vue'
import Router from 'vue-router'
import About from './views/About.vue'
import Clusters from './views/Clusters.vue'
import Annotation from './views/Annotation.vue'
import Overview from './views/Overview.vue'
import Testing from './views/Testing.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'about',
            component: About
        },
        {
            path: '/clusters',
            name: 'clusters',
            component: Clusters

        },
        {
            path: '/annotation',
            name: 'annotator.py',
            component: Annotation
        },
        {
            path: '/overview',
            name: 'overview',
            component: Overview
        },
        {
            path: '/test',
            name: 'test',
            component: Testing
        }
    ]
})
