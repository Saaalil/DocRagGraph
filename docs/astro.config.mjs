import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	integrations: [
		starlight({
			title: 'DocRagGraph',
			customCss: [
				'./src/custom.css',
			],
			sidebar: [
				{
					label: 'Guides',
					items: [
						{ label: 'Architecture', link: '/guides/architecture/' },
					],
				},
			],
		}),
	],
});
