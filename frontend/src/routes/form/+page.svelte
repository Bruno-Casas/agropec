<script>
	import Button from '../../components/Button.svelte';
	import ComboBox from '../../components/ComboBox.svelte';
	import Context from '../../components/Context.svelte';
	import Header from '../../components/Header.svelte';
	import Radio from '../../components/Radio.svelte';
	import TextInput from '../../components/TextInput.svelte';
	import { Bovine } from '../../model/Bovine';
	import { Category } from '../../model/Category';
	import { Color } from '../../model/Color';
	import { Earring } from '../../model/Earring';
	import { faQrcode } from '@fortawesome/free-solid-svg-icons';

	/**
	 * @type {any}
	 */
	let earringIdentifier;

	/**
	 * @param {{ target: EventTarget | null; }} event
	 */
	function onSubmit(event) {
		// @ts-ignore
		const formData = new FormData(event.target);

		formData.forEach(console.log);

		const category = new Category();
		const color = new Color();
		const earring = new Earring();
		const bovine = new Bovine();

		category.id = Number(formData.get('category'));
		category.name = categories.find((o) => o.value === category.id)?.text;

		color.id = Number(formData.get('earringColor'));
		color.alias = colors.find((o) => o.value === color.id)?.text;

		earring.number = Number(formData.get('earringNumber'));
		earring.code = String(formData.get('earringIdentifier'));
		earring.color = color;

		bovine.category = category;
		bovine.sex = Number(formData.get('sex'));
		bovine.weight = Number(formData.get('weight'));
		bovine.earring = earring;

		if (window.pywebview) {
			console.log(window.pywebview);
			window.pywebview.api.store(JSON.stringify(bovine));
			return;
		}
	}

	function cancelar() {
		history.back();
	}

	/**
	 * @param {(arg0: string) => void} valueCallBack
	 */
	function readEarringCode(valueCallBack) {
		if (window.pywebview) {
			window.pywebview.api.get_value().then((resp) => valueCallBack(resp.message));
		}
	}

	const earring = {
		number: undefined,
		value: undefined,
		color: undefined
	};

	const bovine = {
		category: 1,
		weight: 'teste',
		earring: undefined,
		sex: 1
	};

	const categories = [
		{ text: 'Corte', value: 1 },
		{ text: 'Leiteiro', value: 2 }
	];

	const colors = [
		{ text: 'Azul', value: 1 },
		{ text: 'Vermelho', value: 2 }
	];
</script>

<Header />

<Context>
	<main class="main">
		<form class="form" on:submit|preventDefault={onSubmit}>
			<fieldset class="left">
				<TextInput
					label="Número"
					name="earringNumber"
					placeholder="Número do brinco"
					type="number"
					value={earring.number}
				/>
				<ComboBox
					label="Categoria"
					name="category"
					placeholder="Categoria do animal"
					options={categories}
					value={bovine.category}
				/>
				<ComboBox
					label="Cor"
					name="earringColor"
					placeholder="cor do brinco"
					options={colors}
					value={earring.color}
				/>
			</fieldset>
			<fieldset class="right">
				<TextInput
					label="Brinco"
					name="earringIdentifier"
					placeholder="Código do brinco"
					readonly={true}
					actionButon={{
						text: 'Ler código',
						icon: faQrcode,
						action: readEarringCode
					}}
					value={earring.value}
				/>
				<Radio
					label="Sexo"
					name="sex"
					placeholder="Sexo do animal"
					options={[
						{ text: 'Fêmea', value: 0 },
						{ text: 'Macho', value: 1 }
					]}
					value={bovine.sex}
				/>
				<TextInput
					label="Peso"
					name="weight"
					placeholder="Peso do animal"
					type="number"
					value={bovine.weight}
				/>
			</fieldset>

			<div class="footer">
				<Button class="teste" text="Cancelar" preset="secondary" action={cancelar} />
				<Button text="Salvar" type="submit" />
			</div>
		</form>
	</main>
</Context>

<style>
	.main {
		width: 100%;
	}
	.form {
		margin: 70px auto;
		padding: 40px;
		border-radius: 20px;
		width: 80%;
		max-width: 1000px;
		display: grid;
		background-color: #f5f6fb;
		grid-template-columns: 50% 50%;
		grid-template-areas:
			'left right'
			'footer footer';
	}

	.form .left,
	.form .right {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.form .left {
		grid-area: left;
	}

	.form .right {
		grid-area: right;
	}

	.form .footer {
		grid-area: footer;
	}

	.form fieldset,
	.footer {
		margin: 0;
		padding: 0.75em;
		border: none;
	}

	.footer {
		display: flex;
		justify-content: right;
		gap: 20px;
	}
</style>
