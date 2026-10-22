import type { Pathname } from '$app/types';
import type { Component } from 'svelte';
import ClipboardPlus from '@lucide/svelte/icons/clipboard-plus';
import LayoutDashboard from '@lucide/svelte/icons/layout-dashboard';
import Menu from '@lucide/svelte/icons/menu';
import Receipt from '@lucide/svelte/icons/receipt';
import Snowflake from '@lucide/svelte/icons/snowflake';

/** One entry in the bottom tab bar and sidebar. */
export interface NavItem {
	// Typed against real routes so a renamed page fails the type check
	href: Pathname;
	label: string;
	icon: Component;
	// Path prefixes that mark this item active; "/" matches the dashboard only
	matches: string[];
}

/** Screen reached from the More tab, with the milestone that builds it. */
export interface SecondaryDestination {
	href: string;
	label: string;
	milestone: string;
}

// Screens behind the More tab; listed here so More stays active on them
export const secondaryDestinations: SecondaryDestination[] = [
	{ href: '/work', label: 'Work entries', milestone: 'M6' },
	{ href: '/clients', label: 'Clients', milestone: 'M4' },
	{ href: '/invoices', label: 'Invoices', milestone: 'M9' },
	{ href: '/settings', label: 'Settings', milestone: 'M4' },
	{ href: '/reports', label: 'Reports', milestone: 'M11' }
];

// Primary tabs from the PRD layout: Dashboard, Log, Storm, Billing, More
export const primaryNav: NavItem[] = [
	{ href: '/', label: 'Dashboard', icon: LayoutDashboard, matches: ['/'] },
	{ href: '/log', label: 'Log', icon: ClipboardPlus, matches: ['/log'] },
	{ href: '/storms/new', label: 'Storm', icon: Snowflake, matches: ['/storms'] },
	{ href: '/billing', label: 'Billing', icon: Receipt, matches: ['/billing'] },
	{
		href: '/more',
		label: 'More',
		icon: Menu,
		matches: ['/more', ...secondaryDestinations.map((destination) => destination.href)]
	}
];

/**
 * Whether a nav item is the active one for the current path.
 *
 * @param item - nav item to test.
 * @param pathname - current URL path, e.g. "/storms/12".
 * @throws Never.
 * @returns True when the path equals or sits under one of the item's prefixes.
 */
export function isActive(item: NavItem, pathname: string): boolean {
	return item.matches.some((prefix) =>
		// Dashboard matches exactly; everything else also matches nested paths
		prefix === '/' ? pathname === '/' : pathname === prefix || pathname.startsWith(`${prefix}/`)
	);
}
