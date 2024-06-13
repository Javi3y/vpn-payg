import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import HomeView from '@/views/HomeView.vue'
import Page from '@/views/Page.vue'
import Logout from '@/views/Logout.vue'
import InboundsView from '@/views/InboundsView.vue'
import InboundView from '@/views/InboundView.vue'
import BalanceView from '@/views/BalanceView.vue'
const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'home',
			component: Page,
			children: [
				{
					path: '',
					name: 'home',
					component: HomeView
				},
				{
					path: 'inbounds',
					name: 'inbounds',
					component: InboundsView
				},
				{
					path: 'inbound/:id',
					name: 'inbound',
					component: InboundView
				},
				{
					path: 'balance',
					name: 'balance',
					component: BalanceView
				}
			]
		},
		{
			path: '/login',
			name: 'login',
			component: Login
		},
		{
			path: '/logout',
			name: 'logout',
			component: Logout
		}
	]
})

export default router
