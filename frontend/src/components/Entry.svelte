<script>
    import { envJson } from '../components/user-data.store';
    import { USER_API, get, text_area_resize } from '../components/utils.js';
    import Tags from "svelte-tags-input";

    export let key
    export let type
    export let placeholder
    export let value
    export let innerHtml
    export let highlight
    export let metadata

    export let readonly = false;
    export let required = true

    export let rows = 4
    export let color = "#000066"

	let derivedReadonly;
	$: derivedReadonly = readonly || !metadata;

	let newValue = ""
  let keywordList = []
  let promiseListKeyword = new Promise(()=>{})

  $ : {
    if  (type === "keyword") {
      if (!derivedReadonly) {
        promiseListKeyword = get(`${USER_API}/keywords/${$envJson.index_name}/${key}`)
      } else {
        promiseListKeyword = [] // no need of promiseListKeyword
      }
    }
  }
  
    function onDelete(val){
      value = value.filter(item => item !== val)
    }

    function onAdd(){
      value = [...value, newValue]
      newValue = ""
    }

    function handleTags(event) {
        value = event.detail.tags;
    }

    function handleClick(val) {
      if (derivedReadonly) {
        let found = val.match(/(http.*)/g)
        if ( found != null) {
          window.open(found,'_blank')
        } else {
          window.open(`/api/user/files/${$envJson.pjDir}/${val}`,'_blank')
        }

    }
  }
</script>

<div class="entry ">
{#if (key == "title") || (key == "titre")}
  <h2 class="text-3xl ">
    {#if highlight && derivedReadonly }
      <p class="entry-title"> &laquo; {@html highlight} &raquo; </p>
    {:else}
      <textarea class="entry-title" type="text" bind:value={value} {placeholder} readonly={derivedReadonly} />
    {/if}
  </h2>


{:else if type == "date"}
  <label class="align-middle items text-gray-600">
  {@html innerHtml}
</label>
  {#if required}
  
  <input  type="date" bind:value={value} {placeholder} readonly={derivedReadonly} required class='text-gray-600'  />
  {:else}
  <input type="date"  bind:value={value} {placeholder} readonly={derivedReadonly} class='text-gray-600'/>
  {/if}


{:else}
  
  {#if value instanceof Array}
    {#if type === "keyword"}
      {#await promiseListKeyword}
      {:then autoComplete}
          <div class="my-custom-class" >
          <Tags
        		tags={value}
            on:tags={handleTags}
            disable={derivedReadonly}
            placeholder={derivedReadonly ? false : placeholder}
            allowDrop={true}
            allowPaste={true}
            onlyUnique={true}
            autoComplete={autoComplete}
            minChars={1}
            
            />
        </div>
        {/await}

  {:else}
      <ul>
        {#each value as val}
            <li>
              {#if highlight && derivedReadonly}
                  <p> &laquo; {@html val} &raquo; </p>
              {:else}
                {#if type == "text"}
                    <input type="text" bind:value={val} {placeholder} readonly={derivedReadonly} />
                {:else if type == "textarea"}
                    <textarea bind:value={val} {placeholder} readonly={derivedReadonly} />
                {:else if type == "link"}
                    <input class={derivedReadonly ? 'clickable': 'no-clickable'} on:click={handleClick(val)} type='text' bind:value={val} {placeholder} readonly={derivedReadonly} />
                {/if}
                {#if (!derivedReadonly) }
                <button on:click={() => onDelete(val)}>
                  <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M6 2l2-2h4l2 2h4v2H2V2h4zM3 6h14l-1 14H4L3 6zm5 2v10h1V8H8zm3 0v10h1V8h-1z"/></svg>
                  </button>
                {/if}
              {/if}
            </li>
        {/each}
      {#if (!derivedReadonly) }
        <li>
          <input type='text' bind:value={newValue} placeholder="Nouvelle entrée"/>
          <button on:click={onAdd}>
          <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M11 9h4v2h-4v4H9v-4H5V9h4V5h2v4zm-1 11a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/></svg>
          </button>
        </li>
      {/if}
      </ul>
    {/if}
      
  {:else}
    {#if highlight && derivedReadonly}
        <p> &laquo; {@html highlight} &raquo; </p>
    {:else}
      {#if type == "text"}
        <input type="text" bind:value={value} {placeholder} readonly={derivedReadonly} />
      {:else if type == "textarea"}
        <textarea bind:value={value} {placeholder} readonly={derivedReadonly} {rows} />
      {:else if type == "link"}
          <input class={derivedReadonly ? 'clickable' : 'no-clickable' } on:click={handleClick(value)} type='text' bind:value={value} {placeholder} readonly={derivedReadonly} />
      {/if}
    {/if}
  {/if}
{/if}
</div>


<style>
	/* override default Tag style */
	.my-custom-class :global(.svelte-tags-input-tag) {
		background-color: #F0F0F0 !important;
    border-radius: 40px;
    color:#1E1E1E !important;
    margin-right: 1.5em;
    padding-left: 1em;
    padding-right: 1em;
    padding-bottom: 0.5em;
    padding-top: 0.5em;
    margin-bottom: 1em;
    font-size: 14px !important;
	}
	.my-custom-class :global(.svelte-tags-input-layout) {
		border-style: none !important;
		cursor: default !important;
    
	}
	.my-custom-class :global(.svelte-tags-input-layout.sti-layout-disable) {
		background-color: transparent !important;
	}
	.my-custom-class :global(.svelte-tags-input) {
		background: transparent !important;
		cursor: default !important;
    
	}
	.my-custom-class :global(.svelte-tags-input:disabled) {
		background-color: transparent !important;
	}

	.clickable {
		color: blue;
		font-weight: normal;
		cursor: pointer;
	}

	.no-clickable {
		color: blue;
		font-weight: normal;
	}

	.entry-title {
		font-weight: bold;
		margin: 0;
    text-decoration: underline;
	}

	input,
	textarea {
		border: none;
		@apply my-1;
		@apply p-1;
		resize: none;
		vertical-align: middle;
    	}
  

	input:not([type='date']),
	textarea {
		@apply w-full;
    @apply my-0;
    
	}

  ul input:not([type='date']),
	ul textarea {
		@apply w-5/6;
    
	}




	input:read-only,
	textarea:read-only {
		@apply p-0;
		@apply bg-transparent;
	}

	p {
		display: inline;
	}

	ul {
		list-style: disc inside;
	}
</style>
