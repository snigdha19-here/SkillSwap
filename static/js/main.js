/* ===================================================================
   main.js  —  the small conveniences that happen in the browser.

   Everything in this file is OPTIONAL polish. The site works without
   it: every button is part of a real HTML form, and the Flask backend
   does all the actual checking and saving. If this file failed to load,
   you could still use SkillSwap normally.

   The file is split into five small functions, one per feature, and
   they are all started at the very bottom.
   =================================================================== */


/* -------------------------------------------------------------------
   1. SHOW / HIDE PASSWORD
   -------------------------------------------------------------------
   A password box hides what you type. This lets you peek at it, which
   is how you catch a typo before submitting.

   How it works: each toggle button has data-target="password", which is
   the id of the input it belongs to. We swap that input's type between
   "password" (dots) and "text" (readable).
   ------------------------------------------------------------------- */
function setUpPasswordToggles() {

    // Find every button with the class pw-toggle. querySelectorAll gives
    // us a list we can walk through, even if the list is empty.
    var toggles = document.querySelectorAll('.pw-toggle');

    toggles.forEach(function (button) {

        button.addEventListener('click', function () {

            // Which input does this button belong to?
            var inputId = button.getAttribute('data-target');
            var input = document.getElementById(inputId);

            // If the input is missing, do nothing rather than crash.
            if (!input) {
                return;
            }

            var isHidden = (input.type === 'password');

            if (isHidden) {
                input.type = 'text';          // reveal the characters
                button.textContent = 'Hide';
                button.setAttribute('aria-pressed', 'true');
            } else {
                input.type = 'password';      // back to dots
                button.textContent = 'Show';
                button.setAttribute('aria-pressed', 'false');
            }
        });
    });
}


/* -------------------------------------------------------------------
   2. MOBILE NAVBAR TOGGLE
   -------------------------------------------------------------------
   On a phone the menu links are hidden. Pressing the hamburger button
   adds the class nav__menu--open to the menu, and the CSS shows it.

   aria-expanded tells screen readers whether the menu is currently
   open or closed, so we keep it in step with what we see.
   ------------------------------------------------------------------- */
function setUpNavToggle() {

    var button = document.getElementById('navToggle');
    var menu = document.getElementById('navMenu');

    // Both must exist. On a page with no navbar we simply stop here.
    if (!button || !menu) {
        return;
    }

    button.addEventListener('click', function () {

        // classList.toggle adds the class if it is missing and removes
        // it if it is there. It returns true when the class ended up on.
        var isOpen = menu.classList.toggle('nav__menu--open');

        button.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
}


/* -------------------------------------------------------------------
   3. FADE THE FLASH MESSAGES AWAY
   -------------------------------------------------------------------
   Messages like "This email is already registered" have been read after
   a few seconds, so we fade them out to clear the page.

   setTimeout means "run this function later". The number is in
   milliseconds, so 5000 is five seconds.
   ------------------------------------------------------------------- */
function setUpFlashFade() {

    var flashes = document.querySelectorAll('.flash');

    if (flashes.length === 0) {
        return;
    }

    setTimeout(function () {

        flashes.forEach(function (flash) {
            // The CSS rule .flash--gone sets opacity to 0, and the
            // transition in the CSS makes that fade smoothly.
            flash.classList.add('flash--gone');
        });

        // Once the fade has finished (0.6s in the CSS), take the
        // messages out of the layout so they stop using up space.
        setTimeout(function () {
            flashes.forEach(function (flash) {
                flash.style.display = 'none';
            });
        }, 700);

    }, 5000);
}


/* -------------------------------------------------------------------
   4. THE CLICKABLE STAR RATING
   -------------------------------------------------------------------
   The stars are five real radio buttons with the name "stars", each
   wearing a label that looks like a star. Clicking a label already
   ticks its radio button, and the CSS already colours the stars in.
   That all works with JavaScript switched off.

   What we add here is the written confirmation underneath, such as
   "You chose 4 of 5", which is useful when the colours are hard to
   tell apart.
   ------------------------------------------------------------------- */
function setUpStarRatings() {

    // There is one .stars group per session card, so handle each.
    var groups = document.querySelectorAll('.stars');

    groups.forEach(function (group) {

        var inputs = group.querySelectorAll('.stars__input');

        // The readout paragraph is the next thing after the stars.
        var readout = group.parentElement.querySelector('.stars__readout');

        inputs.forEach(function (input) {

            // "change" fires whichever way the radio was ticked: by a
            // mouse click on the star, or by the arrow keys.
            input.addEventListener('change', function () {

                if (!input.checked) {
                    return;
                }

                // Make sure the radio really is the chosen one. Clicking
                // the label does this for us, but setting it here too
                // means the same code works however we got here.
                input.checked = true;

                if (readout) {
                    readout.textContent = 'You chose ' + input.value + ' of 5.';
                }
            });
        });
    });
}


/* -------------------------------------------------------------------
   5. ASK BEFORE SOMETHING CANNOT BE UNDONE
   -------------------------------------------------------------------
   Declining a request, deleting a skill and reporting a session are all
   hard to take back. Those forms carry a data-confirm="..." attribute
   holding the question to ask.

   confirm() shows the browser's own yes/no box. If the person picks
   Cancel we call event.preventDefault(), which stops the form being
   sent, so nothing reaches the server at all.
   ------------------------------------------------------------------- */
function setUpConfirmPrompts() {

    var forms = document.querySelectorAll('form[data-confirm]');

    forms.forEach(function (form) {

        // "submit" fires when the form is about to be sent.
        form.addEventListener('submit', function (event) {

            var question = form.getAttribute('data-confirm');

            if (!confirm(question)) {
                event.preventDefault();
            }
        });
    });
}


/* -------------------------------------------------------------------
   START EVERYTHING
   -------------------------------------------------------------------
   This script sits at the bottom of base.html, so the page already
   exists by the time it runs and we can safely look for elements.
   ------------------------------------------------------------------- */
setUpPasswordToggles();
setUpNavToggle();
setUpFlashFade();
setUpStarRatings();
setUpConfirmPrompts();
