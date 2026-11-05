'use strict';

// Progressive enhancement: navigation, image links and FAQ work without JavaScript.
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const mobileMenu = window.matchMedia('(max-width: 820px)');

function closeMenu() {
  navigation.classList.remove('is-open');
  menuButton.setAttribute('aria-expanded', 'false');
}

menuButton.hidden = false;
document.body.classList.add('js-ready');
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  navigation.classList.toggle('is-open', !expanded);
});
navigation.addEventListener('click', (event) => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
mobileMenu.addEventListener('change', closeMenu);

const projects = [...document.querySelectorAll('.project')];
const filterButtons = [...document.querySelectorAll('[data-filter]')];
const filterStatus = document.querySelector('#filter-status');

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    filterButtons.forEach((filter) => {
      const active = filter === button;
      filter.classList.toggle('active', active);
      filter.setAttribute('aria-pressed', String(active));
    });
    let count = 0;
    projects.forEach((project) => {
      const visible = button.dataset.filter === 'all' || project.dataset.category === button.dataset.filter;
      project.hidden = !visible;
      if (visible) count += 1;
    });
    filterStatus.textContent = `${count} réalisation${count > 1 ? 's' : ''} affichée${count > 1 ? 's' : ''}.`;
  });
});

const projectForm = document.querySelector('#project-form');
function chooseService(value) {
  const choice = [...projectForm.querySelectorAll('[name="project"]')].find((input) => input.value === value);
  if (choice) choice.checked = true;
}
document.querySelectorAll('[data-choose]').forEach((link) => {
  link.addEventListener('click', () => chooseService(link.dataset.choose));
});

const dialog = document.querySelector('#project-dialog');
const dialogImage = document.querySelector('#dialog-image');
const dialogTitle = document.querySelector('#dialog-title');
const dialogKind = document.querySelector('#dialog-kind');
const dialogDescription = document.querySelector('#dialog-description');
const dialogCounter = document.querySelector('#dialog-counter');
const dialogContact = document.querySelector('#dialog-contact');
const previousButton = document.querySelector('#previous-project');
const nextButton = document.querySelector('#next-project');
let openProjects = [];
let currentProject = 0;
let returnFocus = null;

function showProject(index) {
  if (!openProjects.length) return;
  currentProject = (index + openProjects.length) % openProjects.length;
  const link = openProjects[currentProject];
  const sourceImage = link.querySelector('img');
  dialogImage.src = link.getAttribute('href');
  dialogImage.alt = sourceImage.alt;
  dialogTitle.textContent = link.dataset.title;
  dialogKind.textContent = link.dataset.kind;
  dialogDescription.textContent = link.dataset.description;
  dialogCounter.textContent = `${currentProject + 1} / ${openProjects.length}`;
  previousButton.disabled = nextButton.disabled = openProjects.length < 2;
}

if (typeof dialog.showModal === 'function') {
  document.querySelectorAll('.project-open').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      openProjects = projects.filter((project) => !project.hidden).map((project) => project.querySelector('.project-open'));
      returnFocus = link;
      showProject(openProjects.indexOf(link));
      dialog.showModal();
      document.body.classList.add('modal-open');
    });
  });
  previousButton.addEventListener('click', () => showProject(currentProject - 1));
  nextButton.addEventListener('click', () => showProject(currentProject + 1));
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    if (returnFocus) returnFocus.focus({ preventScroll: true });
  });
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showProject(currentProject + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
  dialogContact.addEventListener('click', (event) => {
    event.preventDefault();
    const project = openProjects[currentProject];
    chooseService(project.dataset.service);
    if (!projectForm.elements.message.value.trim()) projectForm.elements.message.value = `J’ai une idée dans l’esprit du projet « ${project.dataset.title} » : `;
    dialog.close();
    window.location.hash = 'contact';
    projectForm.elements.message.focus({ preventScroll: true });
  });
}

// Deliberately local: the demo never sends or saves contact details.
const feedback = document.querySelector('#form-feedback');
projectForm.addEventListener('submit', (event) => {
  event.preventDefault();
  if (!projectForm.reportValidity()) return;
  feedback.textContent = 'Le test a bien fonctionné. Sur votre site, cette demande pourrait arriver dans votre boîte mail. Ici, aucune information n’a été envoyée ni enregistrée.';
  feedback.hidden = false;
  feedback.focus();
});
projectForm.addEventListener('input', () => { feedback.hidden = true; });
projectForm.querySelector('[type="submit"]').disabled = false;


const contactDialog = document.querySelector('#contact-dialog');
let contactReturnFocus = null;

if (typeof contactDialog.showModal === 'function') {
  document.querySelectorAll('a[href="#me-contacter"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      contactReturnFocus = mobileMenu.matches && navigation.contains(link) ? menuButton : link;
      closeMenu();
      contactDialog.showModal();
      document.body.classList.add('modal-open');
    });
  });
  contactDialog.querySelector('.contact-modal-close').addEventListener('click', () => contactDialog.close());
  contactDialog.addEventListener('close', () => {
    if (!document.querySelector('dialog[open]')) document.body.classList.remove('modal-open');
    if (contactReturnFocus) contactReturnFocus.focus({ preventScroll: true });
  });
  contactDialog.addEventListener('click', (event) => {
    if (event.target !== contactDialog) return;
    const bounds = contactDialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) contactDialog.close();
  });
}
