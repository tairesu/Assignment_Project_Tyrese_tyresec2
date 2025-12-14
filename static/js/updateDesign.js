const card = document.querySelector('#card');
const design_input = document.querySelector("input#design_choice");


function preselectDesignChoice(design_id){
    if(design_id != '') {

        let design_btn = $(`button:has(img[data-id=${design_id}])`)[0]
        design_btn.click();
    }
}

function setDesignChoice(button_ele) {
    hideUploadFile();
    child_img_id = button_ele.querySelector("img").dataset['id'];
    child_img_src = button_ele.querySelector("img").src;
    /* Update Card image */
    card.src = child_img_src;
    design_input.value = child_img_id;
}

function showUploadFile() {
    $('#uploadFile').animate({height:'show'},200);
}
function hideUploadFile() {
    $('#uploadFile').animate({height:'hide'},200);
}