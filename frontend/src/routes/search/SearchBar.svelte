<script>
	import Accordion from '../../components/accordion/Accordion.svelte';
	import AccordionItem from '../../components/accordion/AccordionItem.svelte';
	import { cssProps } from '../../components/css-props.action';
	import { userTheme } from '../../components/theme.store';
	import { envJson, itemJson, searchJson } from '../../components/user-data.store';
	import SearchInput from './SearchInput.svelte';
	import SearchKeywordInput from './SearchKeywordInput.svelte';
	import SearchSuggestInput from './SearchSuggestInput.svelte';
	import { promiseSearch } from './stores.js';
	import { flatten, format2ES, search } from '../../components/utils.js';

	let body
	function handleSearch() {
		body = format2ES($itemJson, flatten($searchJson, 2).filter(x => x.type !== "button"), $envJson.index_name)
		$promiseSearch = search(body)
	}
</script>

<div class='search-bar' on:keyup={e => e.key === 'Enter' && handleSearch()}
	use:cssProps={$userTheme.search && $userTheme.search.criteria}>

{#if $searchJson.length > 0}

	<!-- recherche basique, première ligne du tableau -->
	<div class="flex flex-row space-x-3">
		{#each $searchJson[0] as { fields, value, type, placeholder, innerHtml, style, color, suggest }, j}
			{#if type == "button"}
				<div class="flex-none my-auto" >
					<button on:click={handleSearch} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded inline-flex items-center itemJsons-center">
						<svg class="fill-current w-4 h-4 sm:mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/></svg>
						<span class="hidden sm:inline">{innerHtml || "Rechercher"}</span>
					</button>
				</div>
			{:else if type === 'keyword' }
				<SearchKeywordInput bind:value={value} {fields} {placeholder} {color} />
			{:else if type === 'search' && suggest }
				<SearchSuggestInput bind:value={value} {placeholder} {innerHtml} {fields} style="flex-1 my-auto {style}" />
			{:else }
				<SearchInput bind:value {type} {placeholder} {innerHtml} style="flex-1 my-auto {style}" />
			{/if}
		{/each}
	</div>

	<!-- recherche avancée, le reste du tableau dans un accordion -->
	{#if $searchJson.length > 1}
		<Accordion containerClass="mt-4">
			<AccordionItem title="Recherche avancée" buttonStyle="padding-left: 0">
				<div slot="content" class="flex-col space-y-4">
					{#each $searchJson.slice(1) as row, i}
							<div class="flex flex-col sm:flex-row space-x-0 sm:space-x-3 space-y-2 sm:space-y-0">
								{#each row as { fields, value, type, placeholder, innerHtml, style, color, suggest }, j}
									{#if type === 'keyword' }
										<SearchKeywordInput bind:value={value} {fields} {placeholder} {color} {style} />
									{:else if type === 'search' && suggest }
										<SearchSuggestInput bind:value={value} {placeholder} {innerHtml} {style} />
									{:else }
										<SearchInput bind:value={value} {type} {placeholder} {innerHtml} {style} />
									{/if}
								{/each}
							</div>
					{/each}
				</div>
			</AccordionItem>
		</Accordion>
	{/if}

{:else}
	<p>...Attente de la config</p>
{/if}

</div>

<style>
	.search-bar {
		width: 85%;
		border: 1px solid #aaa;
		border-radius: 4px;
		padding: 1em;
		margin: 0 0 1em 0;
		background-color: var(--bg-color);
		float:left;
	}
	.search-bar :global(.suggestion .autocomplete) {
		@apply min-w-0;
	}
</style>
