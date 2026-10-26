/* Show the bounded request count before an Advanced pattern is dispatched. */
(() => {
  "use strict";
  document.addEventListener("input", (event) => {
    const fields = event.target.closest("[data-pattern-fields]");
    const plan = fields && fields.querySelector("[data-request-plan]");
    if (!plan || !plan.dataset.countField) return;
    const field = fields.querySelector(`[name="${plan.dataset.countField}"]`);
    const value = Number(field.value);
    plan.textContent = Number.isInteger(value) && value >= 1 && value <= 5
      ? `Runs ${Number(plan.dataset.countBase) + Number(plan.dataset.countFactor) * value} model requests. No automatic retries. Provider charges apply. Generated reasoning requires your review.`
      : "Choose a depth or round count from 1 to 5 before running.";
  });
})();
