
<script lang="ts">
import { onMount } from 'svelte';

type Order = {
	order_id: number;
	items: Record<string, number>;
};

let orders: Order[] = [];
let total = { burger: 0, fries: 0, drink: 0 };
let userInput = '';
let message = '';
let loading = false;

const API_BASE = 'http://localhost:8000';

async function fetchOrders() {
	const res = await fetch(`${API_BASE}/orders`);
	orders = await res.json();
}

async function fetchTotal() {
	const res = await fetch(`${API_BASE}/orders/total`);
	const data = await res.json();
	total = data.total;
}

async function refresh() {
	await Promise.all([fetchOrders(), fetchTotal()]);
}

onMount(refresh);

async function handleSubmit() {
	if (!userInput.trim()) return;
	loading = true;
	message = '';
	try {
		const res = await fetch(`${API_BASE}/orders`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ text: userInput })
		});
		const data = await res.json();
		if (!res.ok) throw new Error(data.detail || 'Error');
		message = data.message;
		userInput = '';
		await refresh();
	} catch (e: any) {
		message = e.message;
	} finally {
		loading = false;
	}
}
</script>

<main class="max-w-xl mx-auto p-6 space-y-6">
	<h1 class="text-2xl font-bold">Drive-Thru Orders</h1>

	<section class="bg-gray-100 rounded p-4">
		<h2 class="font-semibold mb-2">Total Items Ordered</h2>
		<ul class="flex gap-6">
			<li>Burgers: <span class="font-mono">{total.burger}</span></li>
			<li>Fries: <span class="font-mono">{total.fries}</span></li>
			<li>Drinks: <span class="font-mono">{total.drink}</span></li>
		</ul>
	</section>

	<section class="bg-gray-50 rounded p-4">
		<h2 class="font-semibold mb-2">Placed Orders</h2>
		{#if orders.length === 0}
			<p class="text-gray-500">No orders yet.</p>
		{:else}
			<ul class="space-y-2">
				{#each orders as order}
					<li class="border rounded p-2">
						<span class="font-bold">Order #{order.order_id}:</span>
						<span>
							{Object.entries(order.items).map(([item, qty]) => `${qty} ${item}${qty > 1 ? 's' : ''}`).join(', ')}
						</span>
					</li>
				{/each}
			</ul>
		{/if}
	</section>

	<form class="flex gap-2" on:submit|preventDefault={handleSubmit}>
		<input
			class="flex-1 border rounded px-3 py-2"
			type="text"
			placeholder="Type your order or cancel request..."
			bind:value={userInput}
			disabled={loading}
			autocomplete="off"
		/>
		<button class="bg-blue-600 text-white px-4 py-2 rounded" type="submit" disabled={loading}>
			{loading ? 'Processing...' : 'Submit'}
		</button>
	</form>
	{#if message}
		<div class="mt-2 text-blue-700">{message}</div>
	{/if}
</main>
