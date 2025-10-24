/* Assignment 8.5 */

const redirectDiv = document.querySelector("#redirectDiv");

function toggleRedirectDiv(radioValue) {
	let show_profile = document.querySelector("input#yes").checked;
	if ( show_profile ) { redirectDiv.classList.add("dim-out")}
	else if (!show_profile) { redirectDiv.classList.remove("dim-out") }
}