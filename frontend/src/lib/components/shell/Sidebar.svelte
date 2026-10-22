<!--
	Laptop and tablet navigation: same destinations as the tab bar, shown from 1024 px up.
-->
<script lang="ts">
	import { resolve } from '$app/paths';
	import { cn } from '$lib/utils';
	import { isActive, primaryNav } from './nav';

	let { currentPath }: { currentPath: string } = $props();
</script>

<aside class="fixed inset-y-0 left-0 z-40 hidden w-60 flex-col border-r bg-sidebar lg:flex">
	<p class="px-6 py-5 text-lg font-semibold text-sidebar-foreground">Invoicing</p>
	<nav aria-label="Primary" class="flex-1 px-3">
		<ul class="flex flex-col gap-1">
			{#each primaryNav as item (item.href)}
				{@const active = isActive(item, currentPath)}
				<li>
					<a
						href={resolve(item.href)}
						aria-current={active ? 'page' : undefined}
						class={cn(
							'flex min-h-12 items-center gap-3 rounded-md px-3 text-sm font-medium',
							active
								? 'bg-sidebar-accent text-sidebar-accent-foreground'
								: 'text-sidebar-foreground/80 hover:bg-sidebar-accent/60'
						)}
					>
						<item.icon class="size-5" aria-hidden="true" />
						{item.label}
					</a>
				</li>
			{/each}
		</ul>
	</nav>
</aside>
