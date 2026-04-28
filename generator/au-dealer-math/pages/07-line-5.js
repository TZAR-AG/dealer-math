function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE FIVE OF SEVEN</p>
      <p class="line-number">05</p>
      <h2>"Vehicle ready for collection within 14 business days"</h2>

      <div class="label-block">
        <h3>What it means</h3>
        <p>Lock-in period for the dealer to source/prep.</p>
      </div>

      <div class="label-block">
        <h3>What's hidden</h3>
        <p>If market pricing drops in those 14 days, you're locked at the higher price.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Add a clause: "If retail price drops on equivalent stock, contract repriced to lower."</p>
      </div>
    </div>
  `;
}

module.exports = { render };
