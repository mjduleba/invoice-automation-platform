<script lang="ts">
	import './layout.css';
	import { page } from '$app/state';
	import favicon from '$lib/assets/favicon.svg';
	import BottomNav from '$lib/components/shell/BottomNav.svelte';
	import Sidebar from '$lib/components/shell/Sidebar.svelte';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<Sidebar currentPath={page.url.pathname} />

<!-- Phone: clear the tab bar and notch; laptop: clear the 15rem sidebar -->
<main
	class="min-h-dvh px-4 pt-[calc(1.5rem+env(safe-area-inset-top))] pb-[calc(6rem+env(safe-area-inset-bottom))] lg:pt-8 lg:pr-8 lg:pb-8 lg:pl-[calc(15rem+2rem)]"
>
	<div class="mx-auto max-w-3xl">
		{@render children()}
	</div>
</main>

<BottomNav currentPath={page.url.pathname} />
