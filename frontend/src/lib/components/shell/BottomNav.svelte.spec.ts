import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';
import BottomNav from './BottomNav.svelte';

describe('BottomNav', () => {
	it('renders the five PRD tabs in order', () => {
		render(BottomNav, { currentPath: '/' });

		const labels = screen.getAllByRole('link').map((link) => link.textContent?.trim());
		expect(labels).toEqual(['Dashboard', 'Log', 'Storm', 'Billing', 'More']);
	});

	it('marks only the current tab with aria-current', () => {
		render(BottomNav, { currentPath: '/storms/new' });

		expect(screen.getByRole('link', { name: 'Storm' })).toHaveAttribute('aria-current', 'page');
		const otherTabs = screen
			.getAllByRole('link')
			.filter((link) => link.textContent?.trim() !== 'Storm');
		otherTabs.forEach((link) => expect(link).not.toHaveAttribute('aria-current'));
	});
});
