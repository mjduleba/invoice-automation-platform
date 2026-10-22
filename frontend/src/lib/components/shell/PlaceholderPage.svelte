<!--
	Stand-in for a screen that a later milestone builds; keeps every tab navigable in M1.
-->
<script lang="ts">
	let { title, milestone, summary }: { title: string; milestone: string; summary: string } =
		$props();
</script>

<svelte:head><title>{title} · Invoicing</title></svelte:head>

<h1 class="text-2xl font-semibold">{title}</h1>
<p class="mt-2 text-muted-foreground">{summary}</p>
<p class="mt-4 text-sm text-muted-foreground">Arrives in {milestone}.</p>
