function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE FIVE OF SEVEN</p>
      <p class="line-number">05</p>
      <h2>"Estimated Payout Figure"</h2>
      <p class="parenthetical">(only applies if you have an existing car loan being rolled over)</p>

      <div class="label-block">
        <h3>What it says</h3>
        <p>The amount your existing finance company says is owing on your current car loan.</p>
      </div>

      <div class="label-block">
        <h3>What I saw on the dealer side</h3>
        <p>The word <em>estimated</em> in this line is doing serious work.</p>
        <p>When you trade in a financed car, the dealership pays out your existing loan. The figure on the contract is pulled from your bank's system days before settlement. By the time the actual payout happens, that figure can shift — late fees, daily interest accruals, early-repayment penalties, processing fees. If the actual payout comes back higher than the estimate, the dealership has two options: absorb it or pass it to you. They almost always pass it.</p>
        <p>The more dangerous version is when your existing loan is HIGHER than your trade-in's market value. That's negative equity. Dealerships don't avoid customers with negative equity — they specifically target them, because the rollover into a new finance contract is one of the most profitable structures in the industry.</p>
        <p>In my experience, a customer rolling negative equity into a new loan typically added <strong>$5,000–$15,000+</strong> to the lifetime cost of their next car, hidden inside the monthly repayment.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Get the actual payout figure from your existing bank in writing the day before signing. Compare it to the trade-in figure. If there's a gap, do NOT sign — close the existing loan separately, then start the new deal fresh.</p>
      </div>

      <div class="cta-quote">
        The negative equity rollover is one of the most expensive moves in Australian car buying, and most buyers never realise it happened to them until two years later when their loan is bigger than their car. The full <strong>Negative Equity Trap</strong> breakdown lives on the AU Dealer Math channel. Subscribe.
      </div>
    </div>
  `;
}

module.exports = { render };
