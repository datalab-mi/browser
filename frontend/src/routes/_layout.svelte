<script>
	import { onMount, onDestroy } from 'svelte';
	import { cssProps } from '../components/css-props.action';
	import { userTheme } from '../components/theme.store';
	import { user } from '../components/stores';
	import Logger from '../components/Logger.svelte';
	import LoginForm from '../components/login/LoginForm.svelte';
	import { displayLogin } from '../components/stores.js';
	import Footer from '../layouts/Footer.svelte';
	import Nav from '../layouts/Nav.svelte';

	export let segment;

	let rootNode;
	let mainNode;

	onMount(() => {
		rootNode = document.documentElement;
	})

	$: rootNode && cssProps(rootNode, $userTheme.root);


</script>

{#if $displayLogin }
	<LoginForm />
{/if}


<!-- {#if $user.resources.includes("nav") }
	<Nav {segment} {login} />
{/if}
-->
<Nav {segment} />
<main>
	<div class="">
		<slot />
		<Logger />
	</div>
</main>
<Footer />
