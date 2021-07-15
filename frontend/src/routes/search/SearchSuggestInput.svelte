<script>
	import AutoComplete from 'simple-svelte-autocomplete';
	import { onMount, onDestroy } from 'svelte';
	import { envJson } from '../../components/user-data.store';
	import { httpClient, USER_API } from '../../components/utils.js';

	export let innerHtml = '';
	export let style = '';
	export let placeholder = '';
	export let value = '';
	export let fields = '';

	const http = httpClient();

	const inputId = "suggest-" + Math.floor(Math.random() * 1000);
	const minCharactersToSuggest = 4;
	const valueFieldName = 'text';
	const labelFieldName = 'text';

	// méthodes qui permettent de synchroniser le champ 'value' et le texte du champ <input />
	let onSuggestionInput;
	let onSuggestionSelected;

	onMount(() => {
		onSuggestionInput = (event) => (value = event.target.value);
		onSuggestionSelected = (selected) => (value = selected[valueFieldName]);

		const nestedInput = document.getElementById(inputId);
		nestedInput && nestedInput.addEventListener('input', onSuggestionInput);
	});

	onDestroy(() => {
		const nestedInput = document.getElementById(inputId);
		nestedInput && nestedInput.removeEventListener('input', onSuggestionInput);
	});

	/**
	 * fonction de mapping suggestion => keyword
	 * Le but initial du composant est de conserver uniquement les valeurs contenant le texte du champ <input />,
	 * ce qui est inadapté aux suggestions. C'est pourquoi on renvoie ici le texte du champ.
	 */
	const keywordsFunction = (/* suggestion */) => value || '';

	/**
	 * fonction asynchrone de recherche des suggestions.
	 * Le serveur n'est appelé qu'à partir d'une certaine longueur de chaîne.
	 *
	 * note : on n'utilise pas l'option 'minCharactersToSearch' car elle fonctionne mal avec la validation sur 'Enter',
	 * en effet la première valeur de la dernière liste de suggestions est utilisée, ce n'est pas ce qu'on veut.
	 */
	const searchFunction = async (inputText) => {
		console.debug('MAJ des suggestions');
		if (!inputText || inputText.length < minCharactersToSuggest) {
			return []
		} else {
			const res = await http.fetchJson(`${USER_API}/suggest`, {
					method: 'POST',
					body: JSON.stringify({
						index_name: $envJson.index_name,
						content: inputText,
						fields: fields
					}),
			  })
			if (res.length > 0) {
				res.unshift({"text":inputText})
				return res
			} else {
				return []
			}
		}
	};

</script>

<div class={style}>
	<!-- svelte-ignore a11y-label-has-associated-control -->
	<label class="suggestion">
		{@html innerHtml}
		<AutoComplete
			{placeholder}
			{inputId}
			inputClassName="bg-white focus:outline-none py-4 block w-full "
			{searchFunction}
			{keywordsFunction}
			{labelFieldName}
			{valueFieldName}
			hideArrow={true}
			noResultsText=""
			onChange={onSuggestionSelected}
		/>
	</label>
</div>

<style>
	.suggestion :global(.autocomplete) { width: 100% }
	.suggestion :global(.autocomplete-list-item:first-child) {
		display: none;
		}

</style>
