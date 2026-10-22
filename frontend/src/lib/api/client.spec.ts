import { describe, expect, it } from 'vitest';
import { readCsrfToken, withCsrfHeader } from './client';

// Request to an arbitrary API path with the given method
const requestWith = (method: string): Request =>
	new Request('http://localhost/api/v1/anything', { method });

describe('readCsrfToken', () => {
	it('finds the csrftoken cookie among others', () => {
		expect(readCsrfToken('sessionid=abc; csrftoken=tok123; theme=dark')).toBe('tok123');
	});

	it('returns undefined when the cookie is absent', () => {
		expect(readCsrfToken('sessionid=abc')).toBeUndefined();
		expect(readCsrfToken('')).toBeUndefined();
	});

	it('does not match cookies that only end with the name', () => {
		expect(readCsrfToken('xcsrftoken=nope')).toBeUndefined();
	});
});

describe('withCsrfHeader', () => {
	it('adds the token to unsafe methods', () => {
		for (const method of ['POST', 'PATCH', 'PUT', 'DELETE']) {
			const request = withCsrfHeader(requestWith(method), 'csrftoken=tok123');
			expect(request.headers.get('X-CSRFToken')).toBe('tok123');
		}
	});

	it('leaves safe methods untouched', () => {
		const request = withCsrfHeader(requestWith('GET'), 'csrftoken=tok123');
		expect(request.headers.has('X-CSRFToken')).toBe(false);
	});

	it('sends no header when there is no token yet', () => {
		const request = withCsrfHeader(requestWith('POST'), 'sessionid=abc');
		expect(request.headers.has('X-CSRFToken')).toBe(false);
	});
});
