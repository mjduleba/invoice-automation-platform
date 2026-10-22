import { describe, expect, it } from 'vitest';
import { checkApiHealth } from './health';

// Fake fetch that answers with a fixed status and JSON body
const respondWith =
	(status: number, body: unknown): typeof fetch =>
	async () =>
		new Response(JSON.stringify(body), { status });

describe('checkApiHealth', () => {
	it('reports connected when the API answers status ok', async () => {
		expect(await checkApiHealth(respondWith(200, { status: 'ok' }))).toBe('connected');
	});

	it('reports unreachable when the database check fails', async () => {
		expect(await checkApiHealth(respondWith(503, { status: 'error' }))).toBe('unreachable');
	});

	it('reports unreachable on an unexpected body', async () => {
		expect(await checkApiHealth(respondWith(200, { hello: 'world' }))).toBe('unreachable');
	});

	it('reports unreachable when the network request fails', async () => {
		const failingFetch: typeof fetch = async () => {
			throw new TypeError('Failed to fetch');
		};
		expect(await checkApiHealth(failingFetch)).toBe('unreachable');
	});
});
