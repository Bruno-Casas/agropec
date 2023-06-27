<script>
	import { uid, onClickOutside } from './Context.svelte';
	import './Input.css';

	/**
	 * @type {boolean | undefined}
	 */
	export let disabled = undefined;

	/**
	 * @type {string | undefined}
	 */
	export let label = '';

	/**
	 * @type {string}
	 */
	export let name;

	/**
	 * @type {{text: string; value: any}[]}
	 */
	export let options;

	/**
	 * @type {string | undefined}
	 */
	export let placeholder = undefined;

	/**
	 * @type {boolean | undefined}
	 */
	export let readonly = undefined;

	/**
	 * @type {boolean | undefined}
	 */
	export let error = undefined;

	/**
	 * @type {any}
	 */
	 export let value = undefined;

	export let id = uid();
</script>

<div class="radio">
	<label for={id}>
		{label}
		{#if error}
			<span class="form-validation-error">
				{error}
			</span>
		{/if}
	</label>

	<div class="radio-container">
		<slot name="icon-start" />

        {#each options as option, i (i)}
            <div>
                <input
                    class="radio__input"
                    id="{id}-{i}"
                    {name}
					checked={option.value == value}
                    type="radio"
                    {disabled}
                    autocapitalize="none"
                    autocomplete="off"
                    {readonly}
                    {placeholder}
                    spellcheck="false"
                    value={option.value}
                />
                <label for="{id}-{i}">{option.text}</label>
            </div>
        {/each}
	</div>
</div>

<style>
    .radio-container {
        position: relative;
        padding: 0.85rem 1rem;
        text-align: center;
        display: flex;
        justify-content: space-evenly;
		font-weight: bold;
    }
</style>