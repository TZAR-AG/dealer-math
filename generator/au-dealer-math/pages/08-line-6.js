function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE SIX OF SEVEN</p>
      <p class="line-number">06</p>
      <h2>"Pre-delivery inspection: completed"</h2>

      <div class="label-block">
        <h3>What it means</h3>
        <p>Dealer attests vehicle inspected before handover.</p>
      </div>

      <div class="label-block">
        <h3>What's hidden</h3>
        <p>~30% of PDIs are tick-box, not actual inspections.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Independent pre-delivery inspection. ~$200 from a local mechanic.</p>
      </div>
    </div>
  `;
}

module.exports = { render };
