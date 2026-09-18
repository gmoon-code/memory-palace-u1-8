function esc(v=''){return String(v).replace(/[&<>'\"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','\"':'&quot;'}[ch]))}

export function coursesView(registry,progressByCourse={}){
  const courses=(registry?.courses||[]).filter(c=>c?.student_visible!==false&&c?.status==='available');
  const cards=courses.map((course,index)=>{
    const theme=['yellow','green','turquoise','pink'][index%4];
    const progress=!!progressByCourse[course.course_id];
    return `<article class="card course-choice-card" data-course-theme="${theme}">
      <div class="course-choice-head">
        <span class="course-choice-label">${esc(course.subject||'Science')}</span>
        <span class="course-choice-status">${progress?'In progress':'Available'}</span>
      </div>
      <h2>${esc(course.title)}</h2>
      <p>${esc(course.description||'')}</p>
      <div class="course-choice-meta">
        <span><strong>${esc(course.unit_count||0)}</strong> units</span>
        ${course.level?`<span>${esc(course.level)}</span>`:''}
      </div>
      <button class="${progress?'primary':'secondary'}" data-action="open-course" data-course="${esc(course.course_id)}">${progress?'Continue':'Open'} ${esc(course.short_title||course.title)}</button>
    </article>`;
  }).join('');

  return `<main id="main-content" tabindex="-1" class="stack courses-home" aria-label="The Story Method courses">
    <section class="courses-intro">
      <span class="eyebrow">The Story Method</span>
      <h1>Choose a course</h1>
      <p>Select a science course to open its units, journeys, stories, Review, and Challenge Lab.</p>
    </section>
    <section class="course-choice-section" aria-labelledby="course-choice-title">
      <h2 id="course-choice-title">Courses</h2>
      <div class="course-choice-grid">${cards||'<p class="muted">No courses are available yet.</p>'}</div>
    </section>
  </main>`;
}
