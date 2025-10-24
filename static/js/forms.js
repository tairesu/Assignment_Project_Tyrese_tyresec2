/* Assignment 8.5 */

const redirectDiv = document.querySelector("#redirectDiv");
const redirectUrl = document.querySelector("#id_reroute_url");

function toggleRedirectDiv(radioValue) {
	let show_profile = document.querySelector("input#yes").checked;
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