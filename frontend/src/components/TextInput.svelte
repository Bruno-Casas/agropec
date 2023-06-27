<script>
	import Fa from 'svelte-fa';
	import { uid } from './Context.svelte';
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
	 export let required = undefined;

	/**
	 * @type {boolean | undefined}
	 */
	export let error = undefined;

	/**
	 * @type {any}
	 */
	export let value = undefined;

	/**
	 * @type {string | undefined}
	 */
	 export let type = undefined;

	/**
	 * @type {{
	 * action?: (valueCallBack: (value: any) => void) => void;
	 * icon?: import('@fortawesome/free-solid-svg-icons').IconDefinition;
	 * text: string
	 * } | undefined}
	 */
	export let actionButon = undefined

	export let id = uid();

	function actionWrapper() {
		if (actionButon?.action)
			actionButon.action(v => value = v)
	}

</script>

<div class="input">
	<label for={id}>
		{label}
		{#if error}
			<span class="form-validation-error">
				{error}
			</span>
		{/if}
	</label>

	<div class="input-container">
		<input
			on:focus
			on:blur
			on:input
			class="text__input {readonly === true ? 'readonly' : ''} {actionButon? 'has-action': ''}"
			{id}
			{name}
			{type} 
			value={ value !== undefined ? value : ''}
			{disabled}
			autocapitalize="none"
			autocomplete="off"
			{readonly}
			{placeholder}
			spellcheck="false"
			aria-required={required ? true : undefined}
		/>

		{#if actionButon}
			<button class="action-button" type="button" on:click={actionWrapper}>
				{#if actionButon.icon}
					<Fa icon={actionButon.icon} scale={1} />
				{/if}
				<span>{actionButon.text}</span>
			</button>
		{/if}
	</div>
</div>

<style>
	.input-container {
		display: flex;
	}

	/* Chrome, Safari, Edge, Opera */
	.input-container input::-webkit-outer-spin-button,
	.input-container input::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	/* Firefox */
	.input-container input[type=number] {
		appearance: textfield;
	}

	.action-button {
		border: none;
		border-top-right-radius: 0.36rem;
		border-bottom-right-radius: 0.36rem;
		background-color: #BDC3CB;
	}

	.action-button span {
		white-space: nowrap;
	}

	.input-container .readonly {
		background-color: #EFEFEF;
	}

	.input-container .has-action {
		border-top-right-radius: 0;
		border-bottom-right-radius: 0;
	}

</style>