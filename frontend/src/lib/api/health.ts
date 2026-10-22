import { api, type ApiClient } from './client';

/** Result of probing the backend health endpoint. */
export type ApiHealth = 'connected' | 'unreachable';

/**
 * Probe GET /api/v1/health to confirm the browser can reach Django and its database.
 *
 * @param client - typed API client; injectable for tests.
 * @throws Never; network failures report "unreachable".
 * @returns "connected" when the API answers status ok, else "unreachable".
 */
export async function checkApiHealth(client: ApiClient = api): Promise<ApiHealth> {
	try {
		// A 503 lands in `error`, leaving `data` undefined
		const { data } = await client.GET('/api/v1/health');
		return data?.status === 'ok' ? 'connected' : 'unreachable';
	} catch {
		return 'unreachable';
	}
}
