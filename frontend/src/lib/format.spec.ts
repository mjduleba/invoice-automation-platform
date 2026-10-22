import { describe, expect, it } from 'vitest';
import { formatDate, formatDateTime, formatMoney } from './format';

// Intl may emit narrow no-break spaces; compare on plain spaces
const normalizeSpaces = (text: string): string => text.replace(/\s/g, ' ');

describe('formatMoney', () => {
	it('formats API decimal strings as dollars with cents', () => {
		expect(formatMoney('1234.5')).toBe('$1,234.50');
		expect(formatMoney('0.00')).toBe('$0.00');
		expect(formatMoney(75)).toBe('$75.00');
	});

	it('shows negative amounts with a leading minus', () => {
		expect(formatMoney('-12.30')).toBe('-$12.30');
	});

	it('rejects values that are not amounts', () => {
		expect(() => formatMoney('abc')).toThrow(RangeError);
		expect(() => formatMoney('')).toThrow(RangeError);
		expect(() => formatMoney(Number.NaN)).toThrow(RangeError);
	});
});

describe('formatDate', () => {
	it('keeps the calendar date regardless of the viewer time zone', () => {
		expect(formatDate('2026-11-03')).toBe('Nov 3, 2026');
		expect(formatDate('2026-12-31')).toBe('Dec 31, 2026');
	});

	it('rejects malformed and impossible dates', () => {
		expect(() => formatDate('11/03/2026')).toThrow(RangeError);
		expect(() => formatDate('2026-02-30')).toThrow(RangeError);
	});
});

describe('formatDateTime', () => {
	it('shows timestamps in America/New_York across the DST change', () => {
		// Oct 31 is EDT (UTC-4); Nov 2 is EST (UTC-5)
		expect(normalizeSpaces(formatDateTime('2026-10-31T12:00:00Z'))).toBe('Oct 31, 2026, 8:00 AM');
		expect(normalizeSpaces(formatDateTime('2026-11-02T12:00:00Z'))).toBe('Nov 2, 2026, 7:00 AM');
	});

	it('rejects unparseable timestamps', () => {
		expect(() => formatDateTime('not a time')).toThrow(RangeError);
	});
});
