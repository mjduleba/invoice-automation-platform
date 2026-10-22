<script lang="ts">
	import { secondaryDestinations } from '$lib/components/shell/nav';
</script>

<svelte:head><title>More · Invoicing</title></svelte:head>

<h1 class="text-2xl font-semibold">More</h1>

<!-- Screens not built yet are listed but disabled, with the milestone that adds them -->
<ul class="mt-4 divide-y rounded-lg border">
	{#each secondaryDestinations as destination (destination.href)}
		<li class="flex min-h-12 items-center justify-between px-4 text-muted-foreground">
			<span>{destination.label}</span>
			<span class="text-xs"><span class="sr-only">Coming in </span>{destination.milestone}</span>
		</li>
	{/each}
</ul>
