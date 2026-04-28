function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE ONE OF SEVEN</p>
      <p class="line-number">01</p>
      <h2>"Drive-away price includes all standard on-road costs"</h2>

      <div class="label-block">
        <h3>What it means</h3>
        <p>Stamp duty + rego + LCT + PPSR + dealer delivery.</p>
      </div>

      <div class="label-block">
        <h3>What's hidden</h3>
        <p>Dealer delivery is a markup, not a fee. ~$1,500-3,000 per car. Negotiable.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Ask for the "ex-on-road" price and reverse-engineer the dealer delivery component.</p>
      </div>
    </div>
  `;
}

module.exports = { render };
