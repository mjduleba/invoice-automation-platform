// Display formatters only; billing math stays in the backend as Decimal (BR-01)

const BUSINESS_TIME_ZONE = 'America/New_York';

const usdFormatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });

// Date-only values are calendar dates; format them in UTC so they never shift a day
const calendarDateFormatter = new Intl.DateTimeFormat('en-US', {
	dateStyle: 'medium',
	timeZone: 'UTC'
});

const timestampFormatter = new Intl.DateTimeFormat('en-US', {
	dateStyle: 'medium',
	timeStyle: 'short',
	timeZone: BUSINESS_TIME_ZONE
});

const ISO_DATE_PATTERN = /^(\d{4})-(\d{2})-(\d{2})$/;

/**
 * Format a money amount as US dollars for display.
 *
 * @param amount - API decimal string such as "1234.50", or a number.
 * @throws RangeError when the amount is not a finite number.
 * @returns Display string such as "$1,234.50".
 */
export function formatMoney(amount: string | number): string {
	const numericAmount = typeof amount === 'number' ? amount : Number(amount);
	if (amount === '' || !Number.isFinite(numericAmount)) {
		throw new RangeError(`Not a money amount: ${String(amount)}`);
	}
	return usdFormatter.format(numericAmount);
}

/**
 * Format a calendar date (work date, due date) for display.
 *
 * @param isoDate - date-only string "YYYY-MM-DD".
 * @throws RangeError when the string is not a valid date.
 * @returns Display string such as "Nov 3, 2026".
 */
export function formatDate(isoDate: string): string {
	const parts = ISO_DATE_PATTERN.exec(isoDate);
	if (!parts) {
		throw new RangeError(`Not an ISO date: ${isoDate}`);
	}

	// Build the date in UTC and reject rollovers such as Feb 30
	const [year, month, day] = parts.slice(1).map(Number);
	const date = new Date(Date.UTC(year, month - 1, day));
	if (date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) {
		throw new RangeError(`Not an ISO date: ${isoDate}`);
	}
	return calendarDateFormatter.format(date);
}

/**
 * Format a timestamp (sent at, created at) in the business time zone.
 *
 * @param isoTimestamp - ISO 8601 timestamp with offset, e.g. "2026-11-02T12:00:00Z".
 * @throws RangeError when the timestamp cannot be parsed.
 * @returns Display string in America/New_York, such as "Nov 2, 2026, 7:00 AM".
 */
export function formatDateTime(isoTimestamp: string): string {
	const date = new Date(isoTimestamp);
	if (Number.isNaN(date.getTime())) {
		throw new RangeError(`Not an ISO timestamp: ${isoTimestamp}`);
	}
	return timestampFormatter.format(date);
}
