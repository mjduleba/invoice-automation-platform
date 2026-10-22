<!--
	Phone tab bar: five 48 px+ targets pinned above the home indicator; hidden at 1024 px and up.
-->
<script lang="ts">
	import { resolve } from '$app/paths';
	import { cn } from '$lib/utils';
	import { isActive, primaryNav } from './nav';

	let { currentPath }: { currentPath: string } = $props();
</script>

<nav
	aria-label="Primary"
	class="fixed inset-x-0 bottom-0 z-40 border-t bg-background/95 pb-[env(safe-area-inset-bottom)] backdrop-blur lg:hidden"
>
	<ul class="grid grid-cols-5">
		{#each primaryNav as item (item.href)}
			{@const active = isActive(item, currentPath)}
			<li>
				<!-- Full-cell link keeps the target wide and 64 px tall for gloved thumbs -->
				<a
					href={resolve(item.href)}
					aria-current={active ? 'page' : undefined}
					class={cn(
						'flex min-h-16 flex-col items-center justify-center gap-1 text-xs font-medium',
						active ? 'text-foreground' : 'text-muted-foreground'
					)}
				>
					<item.icon class="size-6" aria-hidden="true" />
					{item.label}
				</a>
			</li>
		{/each}
	</ul>
</nav>
