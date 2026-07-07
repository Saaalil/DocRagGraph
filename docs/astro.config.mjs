import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	integrations: [
		starlight({
			title: 'DocRagGraph',
			customCss: [
				'./src/custom.css',
			],
			social: {
				github: 'https://github.com/Saaalil/DocRagGraph',
			},
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
