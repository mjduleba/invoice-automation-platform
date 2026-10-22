import createClient, { type Client, type ClientOptions, type Middleware } from 'openapi-fetch';
import type { paths } from './schema';

/** Typed client for the Django Ninja API, generated from its OpenAPI schema. */
export type ApiClient = Client<paths>;

// Methods Django's CSRF check skips; every other method needs the token header
const CSRF_SAFE_METHODS = new Set(['GET', 'HEAD', 'OPTIONS', 'TRACE']);
const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';

/**
 * Read Django's CSRF token from a cookie string.
 *
 * @param cookieHeader - cookie string such as document.cookie.
 * @throws Never.
 * @returns Token value, or undefined when the csrftoken cookie is absent.
 */
export function readCsrfToken(cookieHeader: string): string | undefined {
	const prefix = `${CSRF_COOKIE_NAME}=`;
	const cookie = cookieHeader
		.split(';')
		.map((part) => part.trim())
		.find((part) => part.startsWith(prefix));
	return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : undefined;
}

/**
 * Add the X-CSRFToken header to unsafe requests when a token is available.
 *
 * @param request - outgoing request; modified in place.
 * @param cookieHeader - cookie string to read the token from.
 * @throws Never.
 * @returns The same request, for chaining.
 */
export function withCsrfHeader(request: Request, cookieHeader: string): Request {
	const token = readCsrfToken(cookieHeader);
	if (token && !CSRF_SAFE_METHODS.has(request.method.toUpperCase())) {
		request.headers.set(CSRF_HEADER_NAME, token);
	}
	return request;
}

// Session auth: Django rejects writes unless X-CSRFToken matches the csrftoken cookie
const csrfMiddleware: Middleware = {
	onRequest: ({ request }) => withCsrfHeader(request, document.cookie)
};

/**
 * Build a typed API client with CSRF handling attached.
 *
 * @param options - openapi-fetch options; tests inject baseUrl and fetch.
 * @throws Never.
 * @returns Client whose paths, params and responses follow the OpenAPI schema.
 */
export function createApiClient(options: ClientOptions = {}): ApiClient {
	const client = createClient<paths>(options);
	client.use(csrfMiddleware);
	return client;
}

// App-wide client: same origin, and schema paths already include /api/v1
export const api = createApiClient();
