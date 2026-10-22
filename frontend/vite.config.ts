import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { svelteTesting } from '@testing-library/svelte/vite';
import { defineConfig } from 'vitest/config';

// Django origin the dev server forwards backend paths to; Compose overrides it with the service name
const djangoOrigin = process.env.DJANGO_ORIGIN ?? 'http://localhost:8000';

// Backend-owned paths, proxied so the browser sees one origin and session cookies just work
const djangoPaths = ['/api', '/admin', '/static', '/_allauth'];

export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},
			// SPA build: static files Django serves; unknown paths fall back to index.html.
			// precompress writes .gz/.br copies that WhiteNoise serves to supporting browsers
			adapter: adapter({ fallback: 'index.html', precompress: true })
		}),
		svelteTesting()
	],
	server: {
		proxy: Object.fromEntries(djangoPaths.map((path) => [path, djangoOrigin]))
	},
	test: {
		environment: 'jsdom',
		expect: { requireAssertions: true },
		include: ['src/**/*.{test,spec}.{js,ts}'],
		setupFiles: ['./src/vitest-setup.ts']
	}
});
