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
	let notes
	function handleSearch() {
		body = format2ES($itemJson, flatten($searchJson, 2).filter(x => x.type !== "button"), $envJson.index_name)
		$promiseSearch = search(body)
	}

</script>
<div class="background" >
<div id="search" class='search flex flex-col place-items-center ' style="background-image:url('./user/notes.png')" on:keyup={e => e.key === 'Enter' && handleSearch()} >
	<div class="barback flex flex-col w-1/3 px-4"  >
<div>
	<div class='text-3xl text-white left-0 my-8'><b class="border-b-4 pb-4"> Rechercher</b> un rapport  <span class="uppercase">{$envJson.index_name}</span></div>
</div>
{#if $searchJson.length > 0}

	<!-- recherche basique, première ligne du tableau -->
	<div class="flex flex-row space-x-0 gap-0 justify-between bg-white w-full  my-8 h-10">
		
		{#each $searchJson[0] as { fields, value, type, placeholder, innerHtml, style, color, suggest }, j}
			{#if type == "button"}
				<div class="flex-none my-auto bg-white h-8" >
					<button on:click={handleSearch} class="bg-white hover:bg-white text-gray-800">
						<svg class="fill-blue-600 w-6 h-6 sm:mr-2 pt-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/></svg>
					</button>
				</div>
			{:else if type === 'keyword' }
				<SearchKeywordInput bind:value={value} {fields} {placeholder} {color} />
			{:else if type === 'search' && suggest }
				<SearchSuggestInput bind:value={value} {placeholder} {innerHtml} {fields} style="w-2/4  " />
			{:else }
				<SearchInput bind:value {type} {placeholder} {innerHtml} style="" />
			{/if}
		{/each}
		
	</div>
{/if}
</div>
</div>
</div>

<style>
	.search{
		background-size: 22%;
		background-repeat: repeat;
	}
	.background{
		background-color: var(--primary);
	}
	.barback{
		background-color: var(--primary);
	}
</style>
