import {coursesView} from '../frontend/js/views/courses.js';

function assert(ok,message){if(!ok)throw new Error(`COURSE SELECTOR QA FAIL · ${message}`)}

const registry={
  courses:[
    {course_id:'ap-biology',title:'AP Biology',short_title:'AP Biology',subject:'Biology',level:'Advanced Placement',status:'available',student_visible:true,unit_count:8,description:'Visible course'},
    {course_id:'ap-chemistry',title:'AP Chemistry',short_title:'AP Chemistry',subject:'Chemistry',level:'Advanced Placement',status:'development',student_visible:false,unit_count:2,description:'Hidden architecture fixture'}
  ]
};

const html=coursesView(registry,{'ap-biology':true,'ap-chemistry':false});
assert(html.includes('AP Biology'),'available visible AP Biology card is missing');
assert(html.includes('Continue AP Biology'),'AP Biology progress state is not reflected');
assert(!html.includes('AP Chemistry'),'hidden development AP Chemistry fixture leaked into course selector');
assert(!html.includes('ap-chemistry'),'hidden development course id leaked into course selector');

console.log('COURSE SELECTOR HIDDEN-COURSE QA PASS');
