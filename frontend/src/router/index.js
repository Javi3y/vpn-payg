import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import HomeView from '@/views/HomeView.vue'
import Page from '@/views/Page.vue'
import Admin from '@/views/Admin.vue'
import AdminUsers from '@/views/AdminUsers.vue'
import Logout from '@/views/Logout.vue'
import InboundsView from '@/views/InboundsView.vue'
import InboundView from '@/views/InboundView.vue'
import BalanceView from '@/views/BalanceView.vue'
import ClientHistoryView from '@/views/ClientHistoryView.vue'
import PageNotFound from '@/views/PageNotFound.vue'
const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/admin',
			name: 'admin',
			component: Admin,
			meta: { reload: true },
			children: [
				{
					path:'users',
					name:'users',
					component: AdminUsers
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
		},
		{
			path: '/register',
			name: 'register',
			component: Register
		},
		{
			path: '/',
			name: 'home',
			component: Page,
			meta: { reload: true },
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
					path: 'clientHistory/:id',
					name: 'clientHistory',
					component: ClientHistoryView
				},
				{
					path: 'balance',
					name: 'balance',
					component: BalanceView
				},
				{
					path: ':pathMatch(.*)*',
					name: '404',
					component: PageNotFound
				}
			]
		}
	]
})

export default router
