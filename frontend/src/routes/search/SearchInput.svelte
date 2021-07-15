<script>
  export let innerHtml = ""
  export let style = ""
  export let placeholder = ""
  export let value;
  export let type = "text"

  const handleInput = e => {
    // in here, you can switch on type and implement
    // whatever behaviour you need
    value = type.match(/^(number|range)$/)
      ? +e.target.value
      : e.target.value
  };
</script>

  <div class={style}>
    <label> {@html innerHtml}
      <input {type} {value} {placeholder} on:input={handleInput}
        class="bg-white focus:outline-none focus:shadow-outline border border-gray-300 appearance-none leading-normal">
    </label>
  </div>
