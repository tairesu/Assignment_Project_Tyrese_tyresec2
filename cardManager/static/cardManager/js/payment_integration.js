console.log("JS has been summoned")

fetch('/config/')
	.then((result) => {
		return result.json()
	})
	.then((data)=>{
		const stripe = Stripe(data.publishable_key)
		console.log('Pub key @ /config/:', data.publishable_key)  
	})