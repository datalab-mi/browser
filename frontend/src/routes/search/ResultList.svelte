<script>
	import { envJson } from '../../components/user-data.store';
	import ResultItem from './ResultItem.svelte';
	import { list_logger } from '../../components/stores.js';
	import { promiseSearch } from './stores.js';
	import { itemJson } from '../../components/user-data.store';

	let items = [];
	let threshold;
	let resultMessage;
	let message;
	let canBeChange;
	$: canBeChange =  $itemJson.inputs.some((entry) => entry.metadata)

	$: message = $envJson.message ||  "Le document que vous recherchez a peu de chance de se trouver en dessous de cette bande. Veuillez contacter l'<b><a href='mailto:{$envJson.contact}?subject=Demande de consultation'> administrateur ✉️</a></b>."
	//let message = ($envJson.message === undefined) ? dafaultMessage : $envJson.message
	function add_bar(x) {
		items = [];
		threshold = ! (x.hits.some((x) => x._score !== 1)) //test if the request is ranked
		for (const hits of x.hits) {
			hits['key'] = (Math.random() * 1e6) | 0; // Choose random key
			if (hits._score < x.r_threshold && threshold) {
				threshold = false;
				items.push({ _id: 'bar', key: -1 });
			}
			items.push(hits);
		}
	}

	function getResultMessage(results) {
		if ('hits' in results) {
			const nb = results.hits.length;
			switch (nb) {
				case 0: return 'Aucun résultat ne correspond à votre recherche';
				case 1: return '1 résultat correspond à votre recherche';
				default: return nb + ' résultats correspondent à votre recherche';
			}
		}
		return undefined;
	}

	// reactive statement, add_bar function is called whenever the promise changes
	$: {
		$promiseSearch
			.then((searchResults) => {
				add_bar(searchResults);
				resultMessage = getResultMessage(searchResults);
			})
			.catch((err) => {
				list_logger.concat({
					level: 'error',
					message: err,
					ressource: 'search',
				});
			});
	}
</script>
<div class="px-48 " >
{#await $promiseSearch}
	<p>...Attente de la requête</p>
{:then result}
	{#if resultMessage}<p class="mb-4">{resultMessage}</p>{/if}
{/await}

{#if Object.keys($itemJson).length > 0}
	{#if items.length > 0}
		<div class="result-list">
		{#each items as item (item.key)}
			{#if  item._id === "bar"}
				<section class="bar">
					<p>{@html message}</p>
				</section>
			{:else}
				<ResultItem  {... ( ({ _id, _source, _score, highlight }) => ({ _id, _source, _score, highlight, canBeChange }) )(item) }/>
			{/if}
		{/each}
		</div>
	{:else}
		<div class='bg-white p-4 pb-48 shadow'>
			
			<img src='./user/noresult.PNG' class="float-right">
			<h2 class="text-3xl font-bold my-4">Aucun résultat</h2>
			<p class="float-left text-xl ">Malheureusement aucun résultat n'est associé à votre recherche. Essayer de changer les mots-clés que vous avez utilisé.</p>
			
			
		</div>
	{/if}
{:else}
	<p>... Récuperation de la configuration</p>
{/if}

</div>
<style>
img{
	max-width: 20%;
	margin-top: 0;
	
	
}

</style>
