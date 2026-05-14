
 
const scene = document.querySelector('#card-scene');
const card_designs = document.querySelector('#card-designs');

/* To be changed when pointerdown happens */
let currentX = 0;

/* Bool made available to all events */
let isSwiping = false;

/* When user touches the scene */
scene.addEventListener('pointerdown', (e) => {
    console.log('Pointer X Down @', e.clientX);
    isSwiping = true;
    currentX = e.clientX;
})

/* When user drags inside the scene */
scene.addEventListener('pointermove', (e) => {
    console.log('\tNow @ ', e.clientX);
})

/* When user leaves the scene */
scene.addEventListener('pointerup', (e) => {
    console.log('Pointer X Left @ ', e.clientX);
    isSwiping = false;
    deltaX = e.clientX - currentX;
    console.log('Delta X was:', deltaX, ' units')
})
