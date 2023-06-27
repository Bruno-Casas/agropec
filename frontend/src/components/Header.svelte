<script>
    import Fa from 'svelte-fa'
    import { faUserCircle } from '@fortawesome/free-solid-svg-icons'
</script>

<header>
    <h1>Agropec</h1> 
    <Fa icon={faUserCircle} scale={2.5} />
</header>

<style>
	header {
        background-color: #BDC3CB;
		height: 100px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 90px;
        font-family: 'Open Sans', Arial, sans-serif;
	}
</style>