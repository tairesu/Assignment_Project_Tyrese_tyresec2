
 
const scene = document.querySelector('#card-scene');
const card_designs = document.querySelector('#card-designs');

/* To be changed when pointerdown happens */
let startX = 0;

/* Bool made available to all events */
let isSwiping = false;

/* When user touches the scene */
scene.addEventListener('pointerdown', (e) => {
    console.log('Pointer X Down @', e.clientX);
})

/* When user drags inside the scene */
scene.addEventListener('pointermove', (e) => {
    console.log('Now @ ', e.clientX);
})

/* When user leaves the scene */
scene.addEventListener('pointerup', (e) => {
    console.log('Pointer X Left @ ', e.clientX);
})
