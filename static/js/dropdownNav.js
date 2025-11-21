const trigger = document.querySelector("#dropdown-trigger");
const dropdown = document.querySelector("#dropdown-nav");
function toggleDropdownNav(ele) {
    console.log(ele);
    $(trigger).toggleClass('active');
    $(dropdown).toggle();
}