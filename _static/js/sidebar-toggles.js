/**
 * sidebar-toggles.js
 *
 * Sphinx Book Theme shows the hamburger and ToC buttons in the article
 * header, but also leaves hidden duplicates in the PyData navbar.
 * PyData's JS only binds the first match, so tapping the visible buttons
 * shows a tooltip and never opens the sidebar. Forward those clicks to
 * the bound (hidden) controls.
 *
 * Created by Michael Sieler
 * Last updated: 2026-08-13
 */
function initSidebarToggleForward() {
    function forwardExtraToggles(selector) {
        const buttons = document.querySelectorAll(selector);
        if (buttons.length < 2) {
            return;
        }

        const bound = buttons[0];
        for (let i = 1; i < buttons.length; i++) {
            buttons[i].addEventListener(
                "click",
                function (event) {
                    event.preventDefault();
                    event.stopImmediatePropagation();
                    bound.click();
                },
                true
            );
        }
    }

    forwardExtraToggles(".primary-toggle");
    forwardExtraToggles(".secondary-toggle");
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSidebarToggleForward);
} else {
    initSidebarToggleForward();
}
