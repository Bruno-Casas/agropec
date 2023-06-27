<script>
// @ts-nocheck

    import Fa from 'svelte-fa'
    import { faCirclePlus, faPenToSquare } from '@fortawesome/free-solid-svg-icons'

	/**
	 * @type {object}
	 */
	export let data = undefined;

    /**
	 * @type {boolean}
	 */
	export let plus =  false;
</script>

<section class="card">
    {#if plus}
        <a href="/form" class="add">
            <Fa icon={faCirclePlus} scale={2.5} />
        </a>
    {:else}
        <div class="header">
            <span class="label">Brinco</span>
            {#if data.earring.number}
                <span class="main-id" title="Número">N° {data.earring.number}</span>

                {#if data.earring.code}
                    <span class="rfid" title="Código">#{data.earring.code}</span>
                {/if}
            {:else}
                <span class="main-id"title="Código" >#{data.earring.code}</span>
            {/if}
        </div>

        <div>
            <span class="label">Categoria</span>
            <span>{data.category.name}</span>
        </div>

        <div class="secound">
            <span class="label">Peso</span>
            <span>{data.weight}</span>
        </div>

        <div>
            <span class="label">Sexo</span>
            {#if data.sex == 0}
                <span>Fêmea</span>
            {/if}
            {#if data.sex == 1}
                <span>Macho</span>
            {/if}
        </div>

        <div class="secound">
            <span class="label">Cor</span>
            <span>{data.earring.color.alias}</span>
        </div>

        <button class="button" type="button"><Fa icon={faPenToSquare} scale={1.0} /> Editar</button>
    {/if}
</section>

<style>
	.card {
        background-color: #F5F6FB;
        width: 300px;
		height: 240px;
        padding: 20px;
        border-radius: 20px;
	}

    .card div {
        width: 48%;
        display: inline-block;
        margin-bottom: 0.8em;
	}

    .card div  span{
        display: block;
        font-weight: 600;
        font-size: 16px;
        font-family: 'Open Sans';
        font-style: normal;
        color: #252729;
	}

    .card .header {
        width: 100%;
        height: 55px;
    }

    .card .label, .card .rfid {
        font-size: 12px;
        opacity: 0.5;
    }

    .card .rfid {
        font-size: 10px;
    }

    .card .main-id {
        font-size: 20px;
        font-family: 'Open Sans';
        font-style: normal;
    }

    .card:has(> .add) {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .secound {
        padding-left: 1.5rem;
    }
    
    .card .button {
        margin-left: auto;
        display: block;
        background-color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 8px 10px;
        color: #252729;
        font-weight: 600;
    }
</style>
