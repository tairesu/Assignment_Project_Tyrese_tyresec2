console.log("JS has been summoned")

fetch('/config/')
	.then((result) => {
		return result.json()
	})
	.then((data)=>{
		const stripe = Stripe(data.publishable_key)
		console.log('Pub key @ /config/:', data.publishable_key)  

document.querySelector("#activateCardBtn").addEventListener("click", () => {
	fetch("/create-checkout-session/")
		.then((result) => { return result.json() })
		.then((data) => {
			console.log("create-checkout-session fetch data: ", data)
			return stripe.redirectToCheckout({sessionId: data.sessionId})
		})
		.then((res) => {
			console.log("Result from stripe redirect: ", res)
		});
});
});