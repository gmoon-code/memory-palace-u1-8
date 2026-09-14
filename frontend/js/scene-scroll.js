/* Keep scene-to-scene navigation anchored at the story itself.
   Previous/Continue should move the learner to "Follow what happens" in the
   newly rendered scene, not back to the top of the full Learn page. */

function scrollToStoryStart(){
  requestAnimationFrame(()=>{
    const story=document.querySelector('.narrative-section');
    if(!story)return;

    const top=story.getBoundingClientRect().top+window.scrollY-12;
    try{window.scrollTo({top:Math.max(0,top),left:0,behavior:'auto'})}
    catch{window.scrollTo?.(0,Math.max(0,top))}

    const heading=story.querySelector('.section-heading h3');
    if(heading){
      heading.setAttribute('tabindex','-1');
      heading.focus({preventScroll:true});
    }
  });
}

document.addEventListener('click',event=>{
  const button=event.target.closest?.('[data-action="previous-scene"],[data-action="next-scene"]');
  if(!button)return;

  /* Quick Recall has its own navigation context. This behavior is for the
     main story's Previous scene / Continue story controls. */
  if(button.dataset.action==='next-scene'&&document.querySelector('.recall-shell'))return;

  scrollToStoryStart();
});
