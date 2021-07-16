<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { onMount } from 'svelte';
	import { envJson } from '../../components/user-data.store';
	import { promiseSearch } from './stores.js';
	import { itemJson, searchJson } from '../../components/user-data.store';
	import { flatten, format2ES, search } from '../../components/utils.js';
	import SearchBar from './SearchBar.svelte';
	import ResultList from './ResultList.svelte';
	import Aside from './aside.svelte';

	let body
	onMount(async () => {
		//initial search
		if ($envJson.initialSearch) {
			body =  format2ES($itemJson, flatten($searchJson, 2), $envJson.index_name)
			$promiseSearch = search(body)
		}
	});

</script>
<Aside/>
<SearchBar/>
<ResultList/>
