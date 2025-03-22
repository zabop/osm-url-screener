/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

const OVERPASS_URL = 'http://overpass-api.de/api/interpreter?data=';

async function fetchData(relId) {
	try {
		const query = `[out:json][timeout:50];area(${3600000000 + relId})->.searchArea;nwr["contact:website"~".*"](area.searchArea);out body;`;

		console.log('query:');
		console.log(query);
		console.log('query^');

		const resp = await fetch(OVERPASS_URL + query, {
			method: 'GET',
		});

		const data = await resp.json();
		console.log('data:');
		console.log(data);
		const elements = data.elements || [];
		const level0ids = elements.map((e) => `${e.type[0]}${e.id}`);
		const urls = elements.map((e) => e.tags['contact:website']);

		let resp404 = {};
		let respNon404 = {};

		for (let i = 0; i < urls.length; i++) {
			try {
				const response = await fetch(urls[i], { method: 'GET', redirect: 'follow', signal: AbortSignal.timeout(5000) });
				console.log(urls[i], response.status);
				if (response.status === 404) {
					resp404[level0ids[i]] = urls[i];
				} else {
					respNon404[level0ids[i]] = urls[i];
				}
			} catch (error) {
				respNon404[level0ids[i]] = urls[i];
			}
		}

		return { resp404, respNon404 };
	} catch (error) {
		console.error('Error fetching data:', error);
		return { error: error.message };
	}
}

export default {
	async fetch(request, env, ctx) {
		const url = new URL(request.url);
		const relId = parseInt(url.pathname.replace('/', ''), 10);
		if (isNaN(relId)) {
			return new Response('hello world');
		} else {
			const data = await fetchData(relId);
			return new Response(JSON.stringify(data), {
				headers: { 'Content-Type': 'application/json' },
			});
		}
	},
};
