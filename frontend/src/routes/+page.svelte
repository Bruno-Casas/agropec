<script>
// @ts-nocheck

  import Header from '../components/Header.svelte'
  import Card from '../components/Card.svelte'    


  /**
 * @type {never[]}
 */
  let items = []
  async function getAll() {
    try {
      let resp = await fetch('http://127.0.0.1:3000/api/rest/bovine', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      let r = await resp.json()

      console.log(r)

      items = r
    } catch (error) {
    }
//    [
//     {
//         "id": 1,
//         "sex": 1,
//         "category": {
//           "id": 1,
//           "name": "teste descri"
//         },
//         "weight": 1,
//         "earring": {
//             "id": 12,
//             "number": null,
//             "code": "79772985046824122595",
//             "color": {
//                 "code": 1,
//                 "alias": "Teste"
//             }
//         }
//     }
// ]
  }

  getAll()
  setInterval(getAll, 10000)


</script>

<Header/>

<main class="main">
    <Card plus={true}/>
    {#each items as item}
        <Card data={item}/>
    {/each}
</main>

<style>
	.main {
        padding: 125px 65px 0 65px;
        display: flex;
        flex-wrap: wrap;
        gap: 32px;

	}
</style>