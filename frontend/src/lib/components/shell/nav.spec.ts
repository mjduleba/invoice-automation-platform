import { describe, expect, it } from 'vitest';
import { isActive, primaryNav, type NavItem } from './nav';

// Look up a primary tab by its label
const tab = (label: string): NavItem => {
	const item = primaryNav.find((candidate) => candidate.label === label);
	if (!item) throw new Error(`No tab named ${label}`);
	return item;
};

describe('isActive', () => {
	it('matches the dashboard only on the root path', () => {
		expect(isActive(tab('Dashboard'), '/')).toBe(true);
		expect(isActive(tab('Dashboard'), '/log')).toBe(false);
	});

	it('matches nested paths under a tab', () => {
		expect(isActive(tab('Storm'), '/storms/new')).toBe(true);
		expect(isActive(tab('Storm'), '/storms/12')).toBe(true);
		expect(isActive(tab('Billing'), '/billing/7')).toBe(true);
	});

	it('does not match paths that only share a prefix', () => {
		expect(isActive(tab('Log'), '/logout')).toBe(false);
	});

	it('keeps More active on screens reached from it', () => {
		expect(isActive(tab('More'), '/clients/4')).toBe(true);
		expect(isActive(tab('More'), '/invoices')).toBe(true);
	});
});
