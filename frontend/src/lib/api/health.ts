/** Result of probing the backend health endpoint. */
export type ApiHealth = 'connected' | 'unreachable';

/**
 * Probe GET /api/v1/health to confirm the browser can reach Django and its database.
 *
 * @param fetchFn - fetch implementation; injectable for tests.
 * @throws Never; network and parse failures report "unreachable".
 * @returns "connected" when the API answers status ok, else "unreachable".
 */
export async function checkApiHealth(fetchFn: typeof fetch = fetch): Promise<ApiHealth> {
	try {
		const response = await fetchFn('/api/v1/health', { headers: { Accept: 'application/json' } });
		if (!response.ok) {
			return 'unreachable';
		}

		// Only an explicit "ok" body counts; anything else is treated as down
		const body: unknown = await response.json();
		const isOk =
			typeof body === 'object' && body !== null && 'status' in body && body.status === 'ok';
		return isOk ? 'connected' : 'unreachable';
	} catch {
		return 'unreachable';
	}
}
