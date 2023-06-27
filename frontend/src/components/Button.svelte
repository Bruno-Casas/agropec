<script>
    /**
	 * @type {string}
	 */
    export let text;

    /**
	 * @type {(() => void) | null | undefined}
	 */
    export let action = undefined;

    /**
	 * @type {"button" | "submit" | "reset" | null | undefined}
	 */
    export let type = 'button';

    /**
	 * @type {"primary" | "secondary" | null | undefined}
	 */
    export let preset = 'primary' ;

    /**
	 * @type {string}
	 */
    let clazz = '';
	export { clazz as class };

    function onClickWrapper() {
        if (action)
        action()
    }
</script>

<button on:click={onClickWrapper} class="{preset} button {clazz}" type={type}>{text}</button>

<style>
    .button {
        width: 150px;
        height: 45px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 1em;
        outline: none;
        border: none;
    }

    .primary {
        background: #BDC3CB;  
    }

	.secondary {
        background: #FFFFFF;
    }
</style>