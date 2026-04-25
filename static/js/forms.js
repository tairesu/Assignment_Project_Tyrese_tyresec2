/* Assignment 8.5 */

const redirectDiv = document.querySelector("#redirectDiv");
const redirectUrl = document.querySelector("#reroute_url");

function toggleRedirectDiv(radioValue) {
	console.log(radioValue);
	let show_profile = document.querySelector("select#id_show_profile").value == "True";
	if ( show_profile ) {
		redirectDiv.classList.add("dim-out");
		redirectUrl.value = "";
		redirectUrl.style.borderColor = "";
		if (document.querySelector("#redirectDiv ul.errorlist") != null ){
			document.querySelector("#redirectDiv ul.errorlist").remove();
		}


	}
	else if (!show_profile) { redirectDiv.classList.remove("dim-out") }
}

/* Moving the button to action tray block 

*/

let submitForm = (buttonName) => {
	document.querySelector(`form#${buttonName}Form`) && document.querySelector(`form#${buttonName}Form`).submit()
}