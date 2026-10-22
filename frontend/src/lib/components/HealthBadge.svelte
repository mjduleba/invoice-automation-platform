<!--
	Shows whether the browser can reach Django and its database; retry when it cannot.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import { checkApiHealth, type ApiHealth } from '$lib/api/health';
	import { Badge } from '$lib/components/ui/badge';
	import { Button } from '$lib/components/ui/button';

	let health = $state<ApiHealth | 'checking'>('checking');

	// Re-probe the API, showing "checking" while the request is in flight
	async function refresh(): Promise<void> {
		health = 'checking';
		health = await checkApiHealth();
	}

	onMount(refresh);
</script>

<div class="flex items-center gap-3" role="status" aria-live="polite">
	{#if health === 'checking'}
		<Badge variant="outline">Checking API…</Badge>
	{:else if health === 'connected'}
		<Badge variant="secondary">API connected</Badge>
	{:else}
		<Badge variant="destructive">API unreachable</Badge>
		<Button variant="outline" class="min-h-12" onclick={refresh}>Retry</Button>
	{/if}
</div>
