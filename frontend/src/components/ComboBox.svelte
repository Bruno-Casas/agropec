<script>
	import { uid, onClickOutside } from './Context.svelte';
	import './Input.css';

	/**
	 * @type {boolean | undefined}
	 */
	export let disabled = undefined;

	/**
	 * @type {boolean | undefined}
	 */
	export let error = undefined;

	export let id = uid();
	export let label = '';

	/**
	 * @type {string}
	 */
	export let name;

	/**
	 * @type {any[]}
	 */
	export let options = [];

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
	 * @type {any}
	 */
	export let value = '';

	export let filter = (/** @type {string} */ text) => {
		const sanitized = text.trim().toLowerCase();

		return options.reduce((a, o) => {
			let match;

			if (o.options) {
				const options = o.options.filter((o) => o.text.toLowerCase().includes(sanitized));

				if (options.length) {
					match = { ...o, options };
				}
			} else if (o.text.toLowerCase().includes(sanitized)) {
				match = o;
			}

			match && a.push(match);

			return a;
		}, []);
	};

	/**
	 * @type {HTMLUListElement}
	 */
	let listElement;
	/**
	 * @type {HTMLInputElement}
	 */
	let inputElement;

	/**
	 * @type {HTMLInputElement}
	 */
	let valueInput;

	/**
	 * @type {string | ArrayLike<any>}
	 */
	let list = [];

	let isListOpen = false;

	/**
	 * @type {{ text: any; value?: any; }}
	 */
	let selectedOption;

	/**
	 * @param {KeyboardEvent} event
	 */
	async function onInputKeyup(event) {
		switch (event.key) {
			case 'Escape':
			case 'ArrowUp':
			case 'ArrowLeft':
			case 'ArrowRight':
			case 'Enter':
			case 'Tab':
			case 'Shift':
				break;
			case 'ArrowDown':
				await showList(event.target.value);
				listElement.querySelector(`[role="option"]:not([aria-disabled="true"])`)?.focus();

				event.preventDefault();
				event.stopPropagation();
				break;

			default:
				await showList(event.target.value);
		}
	}

	/**
	 * @param {{ key: any; preventDefault: () => void; stopPropagation: () => void; }} event
	 */
	function onInputKeydown(event) {
		let flag = false;

		switch (event.key) {
			case 'Escape':
				hideList();
				flag = true;
				break;

			case 'Tab':
				hideList();
				break;
		}

		if (flag) {
			event.preventDefault();
			event.stopPropagation();
		}
	}

	/**
	 * @param {MouseEvent} event
	 */
	async function onInputClick(event) {
		await showList(event.target.value);
		// Scroll selected option into view.
		listElement.querySelector(`[role="option"][data-value="${value}"]`)?.scrollIntoView();
	}

	/**
	 * @param {{ target: { matches: (arg0: string) => any; }; }} event
	 */
	function onOptionClick(event) {
		if (!event.target.matches(`[role="option"]:not([aria-disabled="true"])`)) return;

		selectOption(event.target);
		hideList();
	}

	/**
	 * @param {{ key: any; target: { previousElementSibling: any; nextElementSibling: any; }; preventDefault: () => void; stopPropagation: () => void; }} event
	 */
	function onListKeyDown(event) {
		let flag = false;

		switch (event.key) {
			case 'ArrowUp':
				let prevOptionElement = event.target.previousElementSibling;

				while (prevOptionElement) {
					if (prevOptionElement.matches(`[role="option"]:not([aria-disabled="true"])`)) break;
					prevOptionElement = prevOptionElement.previousElementSibling;
				}

				prevOptionElement?.focus();
				flag = true;
				break;

			case 'ArrowDown':
				let nextOptionElement = event.target.nextElementSibling;

				while (nextOptionElement) {
					if (nextOptionElement.matches(`[role="option"]:not([aria-disabled="true"])`)) break;
					nextOptionElement = nextOptionElement.nextElementSibling;
				}

				nextOptionElement?.focus();
				flag = true;
				break;

			case 'Enter':
				selectOption(event.target);
				hideList();
				flag = true;
				break;

			case 'Escape':
				hideList();
				flag = true;
				break;

			case 'Tab':
				hideList();
				break;

			default:
				inputElement.focus();
		}

		if (flag) {
			event.preventDefault();
			event.stopPropagation();
		}
	}

	/**
	 * @param {string} inputValue
	 */
	async function showList(inputValue) {
		const isExactMatch = options.some((o) =>
			o.options ? o.options.some((o) => o.text === inputValue) : o.text === inputValue
		);

		list = inputValue === '' || isExactMatch ? options : await filter(inputValue);
		isListOpen = true;
	}

	function hideList() {
		if (!isListOpen) return;

		console.log(selectedOption);
		if (selectedOption) {
			inputElement.value = selectedOption.text;
			valueInput.value = selectedOption.value;
		}

		isListOpen = false;
		inputElement.focus();
	}

	/**
	 * @param {{ matches?: (arg0: string) => any; previousElementSibling?: any; nextElementSibling?: any; dataset?: any; }} optionElement
	 */
	function selectOption(optionElement) {
		value = optionElement.dataset.value;

		selectedOption = {
			text: optionElement.dataset.text,
			value: optionElement.dataset.value
		};
	}
	function setTextValue(ele) {
		const option = options.find(o => o.value === value)

		if (option)
			return option.text

		return ''
	}

</script>

<div class="input">
	<label class="combobox__label label" for={id}>
		{label}
		{#if error}
			<span class="form-validation-error">
				{error}
			</span>
		{/if}
	</label>

	<div class="input-container" use:onClickOutside={hideList}>
		<slot name="icon-start" />

		<input bind:this={valueInput} type="hidden" id="{id}-value" name={name} value={value ? value : ''}>
		<input
			bind:this={inputElement}
			on:focus
			on:blur
			on:input
			on:keyup={onInputKeyup}
			on:keydown={onInputKeydown}
			on:mousedown={onInputClick}
			value={setTextValue(value)}
			class="combobox__input"
			{id}
			type="text"
			{disabled}
			autocapitalize="none"
			autocomplete="off"
			{readonly}
			{placeholder}
			spellcheck="false"
			role="combobox"
			aria-autocomplete="list"
			aria-expanded={isListOpen}
			aria-required={required ? 'true' : undefined}
		/>

		<ul
			class="combobox__list"
			role="listbox"
			aria-label={label}
			hidden={!isListOpen}
			on:click={onOptionClick}
			on:keydown={onListKeyDown}
			bind:this={listElement}
		>
			{#each list as option (option)}
				{#if option.options}
					<li class="list__option-heading">
						<slot name="group" group={option}>
							{option.text}
						</slot>
					</li>
					{#each option.options as option (option)}
						<li
							class="list__option"
							class:--disabled={option.disabled}
							role="option"
							tabindex={option.disabled ? undefined : '-1'}
							data-text={option.text}
							data-value={option.value}
							aria-selected={value === option.value}
							aria-disabled={option.disabled}
						>
							<slot name="option" {option}>
								{option.text}
							</slot>
							{#if option.value === value}
								<svg viewBox="0 0 24 24" class="icon">
									<polyline points="20 6 9 17 4 12" />
								</svg>
							{/if}
						</li>
					{/each}
				{:else}
					<li
						class="list__option"
						class:--disabled={option.disabled}
						role="option"
						tabindex={option.disabled === true ? undefined : '-1'}
						data-text={option.text}
						data-value={option.value}
						aria-selected={value === option.value}
						aria-disabled={option.disabled}
					>
						<slot name="option" {option}>
							{option.text}
						</slot>
						{#if option.value === value}
							<svg viewBox="0 0 24 24" class="icon">
								<polyline points="20 6 9 17 4 12" />
							</svg>
						{/if}
					</li>
				{/if}
			{:else}
				<li class="list__no-results">No results available</li>
			{/each}
		</ul>

		<div class="visually-hidden" role="status" aria-live="polite">
			{list.length} results available.
		</div>
	</div>
</div>

<style>
	.combobox__input:focus {
		outline: none;
	}

	.combobox__list {
		/* Reset */
		list-style: none;
		margin: 0;
		padding: 0.3rem;
		/* Position and Size */
		position: absolute;
		inset-inline-start: 0;
		inset-block-start: calc(100% + 0.3rem);
		min-width: 100%;
		max-height: 40vh;
		overflow-y: auto;
		-webkit-overflow-scrolling: touch;
		z-index: 100;

		background-color: var(--background-color);
		border-radius: 0.3em;
		border: 0.175rem solid var(--accent-color);
		box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
	}

	.list__option-heading {
		font-size: 0.9em;
		padding-inline: 1rem;
		padding-block-start: 0.4rem;
		color: gray;
	}

	.list__no-results {
		padding: 0.8rem 1rem;
	}

	.list__option {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.8rem 1rem;
		border: 0.2rem solid transparent;
		border-radius: 0.3rem;
	}

	.list__option > :global(*) {
		pointer-events: none;
	}

	.list__option.--disabled {
		pointer-events: none;
		opacity: 0.4;
	}

	.list__option:focus,
	.list__option:not([aria-disabled='true']):hover {
		outline: none;
		cursor: pointer;
		background-color: rgba(0, 0, 0, 0.1);
	}

	.list__option:active {
		cursor: pointer;
		outline: none;
		color: white;
		background-color: var(--accent-color) !important;
	}

	.list__option:focus :global(svg),
	.list__option:hover :global(svg) {
		--icon-color: white !important;
	}
</style>
