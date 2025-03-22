/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

const axios = require('axios');

const query = '[out:json][timeout:50];' + 'area(3601690324)->.searchArea;' + 'nwr["contact:website"~".*"](area.searchArea);' + 'out body;';

const OVERPASS_URL = 'http://overpass-api.de/api/interpreter';

async function fetchData() {
	try {
		const resp = await axios.post(OVERPASS_URL, new URLSearchParams({ data: query }));
		const elements = resp.data.elements;

		const level0ids = elements.map((e) => `${e.type[0]}${e.id}`);
		const urls = elements.map((e) => e.tags['contact:website']);

		let resp404 = {};
		let respNon404 = {};

		for (let i = 0; i < urls.length; i++) {
			try {
				const response = await axios.head(urls[i], { maxRedirects: 3, timeout: 3000 });
				if (response.status === 404) {
					resp404[level0ids[i]] = urls[i];
				} else {
					respNon404[level0ids[i]] = urls[i];
				}
			} catch (error) {
				respNon404[level0ids[i]] = urls[i];
			}
		}

		const res = { resp404, respNon404 };
		return res;
	} catch (error) {
		console.error('Error fetching data:', error);
	}
}

export default {
	async fetch(request, env, ctx) {
		const data = await fetchData();
		return new Response(JSON.stringify(data), {
			headers: {
				'content-type': 'application/json',
			},
		});
	},
};
