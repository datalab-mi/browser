<script>
	import { list_logger, user  } from '../stores.js';
	import { synonym  } from '../utils.js';
	import SynonymRow from './SynonymRow.svelte';
	import VirtualList from '../VirtualList.svelte';
  import { onDestroy } from 'svelte'

	import { contextKey } from './synonym.js';
	import { setContext } from 'svelte';
	import { writable } from 'svelte/store';

	export let list_synonym = writable([]);
	setContext(contextKey, list_synonym);

	export let filename;
	export let meta;
	let GetPromise = new Promise(()=>{});

	let isAdd = false;
	let readonly = true;
	let send = false;

	let start;
	let end;
	let key;

	let list_synonym_filter;
	let filterRow = Object.assign({}, ...meta.map((x) => ({[x.key]: ''})));
	let totalSize = meta.reduce((tot, x) => tot + parseInt(x.size), 0)

	let errors = {};

	const keys_to_keep = meta.map(item => item.key);
	keys_to_keep.push('key') // Add row number to the list of key to keep

	GetPromise = synonym('GET', filterRow, filename)
	GetPromise.then((list) => {
		$list_synonym = list.map(element => Object.assign({}, ...keys_to_keep.map(key => ({[key]: element[key]}))))
	})

const handleSubmit = () => {
	errors = {};
	synonym('PUT', filterRow, filename)
		.then((list) => {
			$list_synonym = list.map(element => Object.assign({}, ...keys_to_keep.map(key => ({[key]: element[key]}))))
			list_logger.concat({level: "success", message: "Entrée ajoutée avec succès! ", ressource: "upload"})
			filterRow = Object.assign({}, ...meta.map((x) => ({[x.key]: ''})));
		})
		.catch(err => {
			list_logger.concat({level: "error", message: err, ressource: "upload"})
		})
	// reset filter
	filterRow = Object.assign({}, ...meta.map((x) => ({[x.key]: ''})));
}

function handleAdd() {
	isAdd = !isAdd;
}

$: { // filter $list_synonym with filterRow on its keys (expressionA, expressionB...)
	list_synonym_filter = $list_synonym.filter(
		item => Object.keys(filterRow).every((key) => item[key].toLowerCase().includes(filterRow[key].toLowerCase()))
	)
}

onDestroy(() => $list_synonym = [])

</script>

<div class='containerVL'>
	{#await GetPromise}
	<p>...Attente de la requête</p>
	{:then status}

		<div class="inline-flex bg-{(isAdd) ? 'white': 'gray'}-200 w-full">
			<div class="inline-flex" style="flex-grow: 1">
			{#each meta as {key, type, placeholder, value, innerHtml, size} }
				<div class="flex-auto w-{size}/{totalSize} text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
					<input type="search" bind:value={filterRow[key]} placeholder={(isAdd) ? placeholder: 'recherche'} >
				</div>
			{/each}
			</div>

			{#if ($user.role === "admin") }
				<div class="flex justify-around w-1/6 px-4 py-2 m-2">
					{#if (isAdd)}
						{#if Object.keys(filterRow).every((key) => filterRow[key] != '') }
							<button on:click={handleSubmit} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
								<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
								<span>SOUMETTRE</span>
							</button>
						{:else}
							<button disabled class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
								<svg class="fill-curr
								ent w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
								<span>SOUMETTRE</span>
							</button>
						{/if}
						<button on:click="{() => isAdd = !isAdd}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-2 rounded inline-flex items-center">
							<svg class="fill-current w-4 h-4 mr-2" svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zM11.4 10l2.83-2.83-1.41-1.41L10 8.59 7.17 5.76 5.76 7.17 8.59 10l-2.83 2.83 1.41 1.41L10 11.41l2.83 2.83 1.41-1.41L11.41 10z"/></svg>
						</button>

					{:else}
					<button on:click={handleAdd} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
						<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M11 9h4v2h-4v4H9v-4H5V9h4V5h2v4zm-1 11a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/></svg>
						<span>AJOUTER</span>
					</button>
					{/if}
				</div>
			{/if}
			<div class="w-2"/>
		</div>

		<VirtualList height="90%" items={list_synonym_filter} let:item>
			<SynonymRow {filename} {item} {meta} {totalSize} />
		</VirtualList>

	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</div>

<style>

	.container {
		width: 90%;
	}

	.containerVL {
		min-height: 200px;
		height: calc(60vh)
	}

	.value {
		width: 80%
	}

	.key {
		width: 20%
	}
	th input
	{
    width: 100%;
	}
	input {
		border:none;
		width: 90%;
		resize: none;
		background-color: inherit;
	 }
	table {
  border-collapse: separate;
	table-layout: fixed;
  width: 100%;
	}

	th, td {
  text-align: left;
  padding: 8px;
	white-space:wrap;
}

	thead th {
		 position: sticky; top: 0;
	 }



</style>
