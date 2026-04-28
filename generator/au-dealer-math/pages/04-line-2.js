function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE TWO OF SEVEN</p>
      <p class="line-number">02</p>
      <h2>"Trade-in value: as inspected"</h2>

      <div class="label-block">
        <h3>What it means</h3>
        <p>The figure you signed for is the figure they pay.</p>
      </div>

      <div class="label-block">
        <h3>What's hidden</h3>
        <p>Dealers reassess "as inspected" and reduce on settlement if you're locked in.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Get the trade figure agreed in writing BEFORE signing the new-car contract.</p>
      </div>
    </div>
  `;
}

module.exports = { render };
