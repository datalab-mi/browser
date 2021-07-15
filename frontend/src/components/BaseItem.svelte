<script>
	import { cssProps } from '../components/css-props.action';

	export let id;
	export let componentCssProps = undefined
</script>

<section {id} use:cssProps={componentCssProps} class="base-item rounded-sm p-2 sm:p-4 bg-white shadow my-10">
	<slot name="fields" />

	<div class="flex justify-between">
		<slot name="buttons" />
		<slot name="score" />
	</div>
</section>

<style>
</style>
