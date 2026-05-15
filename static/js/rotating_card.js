
 
const scene = document.querySelector('#card-scene');
const card_designs = document.querySelector('#card-designs');

/* To be changed when pointerdown happens */
let currentX = 0;
let currentRotation = 0;
let isSwiping = false;

/* Bool made available to all events */

const getRotateY = () => {
    rotateY_value = card_designs.style.transform; // RotateY(5deg)
    rotateY_int = rotateY_value.match('-?[0-9]{1,}') && parseInt(rotateY_value.match('-?[0-9]{1,}')[0]);
    return rotateY_int;
};
const setRotateY = (deltaRotate) => {
    currentRotation = getRotateY() + (deltaRotate);
    card_designs.style.transform = `rotateY(${ currentRotation }deg)`;
};
/* When user touches the scene */
scene.addEventListener('pointerdown', (e) => {
    //console.log('Pointer X Down @', e.clientX);
    isSwiping = true;
    currentX = e.clientX;
})

/* When user drags inside the scene */
scene.addEventListener('pointermove', (e) => {
    if (!isSwiping) return;
    deltaX = e.clientX - currentX;
    currentX = e.clientX;
    setRotateY(deltaX)
    console.log(' pointerx=', currentX, '\nDelta pointerx=:', deltaX,  '\ne.pageX=', e.pageX, '\nele rotation=', currentRotation)
})

/* When user leaves the scene */
scene.addEventListener('pointerup', (e) => {
    console.log('Pointer X Left @ ', e.clientX);
    isSwiping = false;
    
})
