import { describe, expect, it } from 'vitest';
import { createApiClient } from './client';
import { checkApiHealth } from './health';

// Typed client whose fetch answers with a fixed status and JSON body
const clientRespondingWith = (status: number, body: unknown) =>
	createApiClient({
		baseUrl: 'http://localhost',
		fetch: async () =>
			new Response(JSON.stringify(body), {
				status,
				headers: { 'Content-Type': 'application/json' }
			})
	});

describe('checkApiHealth', () => {
	it('reports connected when the API answers status ok', async () => {
		expect(await checkApiHealth(clientRespondingWith(200, { status: 'ok' }))).toBe('connected');
	});

	it('reports unreachable when the database check fails', async () => {
		expect(await checkApiHealth(clientRespondingWith(503, { status: 'error' }))).toBe(
			'unreachable'
		);
	});

	it('reports unreachable on an unexpected body', async () => {
		expect(await checkApiHealth(clientRespondingWith(200, { hello: 'world' }))).toBe('unreachable');
	});

	it('reports unreachable when the network request fails', async () => {
		const offlineClient = createApiClient({
			baseUrl: 'http://localhost',
			fetch: async () => {
				throw new TypeError('Failed to fetch');
			}
		});
		expect(await checkApiHealth(offlineClient)).toBe('unreachable');
	});
});
