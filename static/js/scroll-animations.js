const hero = document.querySelector('#hero');
const demo = document.querySelector('#phone-demo');

var prevRatio = 1.0;
/* Intersection observers will be used to observe scroll events  */
const options = {
    'root' : null,
    'threshold' : 0.3,
};

const triggerDemo = () => {
    demo && demo.classList.add('slideTapPhone'); 
};
const demoObserver = new IntersectionObserver((entries, opts)=>{
    console.log(entries);
    /* entries is an array of observer Entries which a key of isIntersecting and intersection Ratio*/
    entries.forEach((entry)=>{
        prevRatio = entry.intersectionRatio;
        /* is intersecting is true when elem starts visible or about to be visible at the threshold */
        /* i want to trigger demo when #hero is not intersecting and intersectionRation is <1  */
        if (!entry.isIntersecting && prevRatio < 1.0) {
            triggerDemo();
        }
    });
}, options)

demoObserver.observe(hero);
