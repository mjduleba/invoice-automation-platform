<script lang="ts">
	import HealthBadge from '$lib/components/HealthBadge.svelte';
</script>

<svelte:head><title>Dashboard · Invoicing</title></svelte:head>

<h1 class="text-2xl font-semibold">Dashboard</h1>
<p class="mt-2 text-muted-foreground">
	Outstanding balances, unbilled work and revenue arrive in M10.
</p>

<div class="mt-6">
	<HealthBadge />
</div>
