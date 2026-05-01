function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE TWO OF SEVEN</p>
      <p class="line-number">02</p>
      <h2>"Trade-In Value: As Inspected"</h2>

      <div class="label-block">
        <h3>What it says</h3>
        <p>The figure you signed for is the figure they pay.</p>
      </div>

      <div class="label-block">
        <h3>What I saw on the dealer side</h3>
        <p>What you signed isn't always what you get. Dealers can — and do — reassess a trade-in "as inspected" after the deal is locked, dropping the figure on the day of changeover. By then you're emotionally and logistically committed to the new car. The dealership knows it.</p>
        <p>The line itself is just the surface mechanic. The actual play happens earlier — before you ever sit down to sign — in a sequence of moves I call <strong>the Walk-Around Doubt-Plant</strong>:</p>
        <ul>
          <li>The salesperson does a slow inspection of your trade and verbally catalogues flaws (real ones, exaggerated ones, sometimes invented ones).</li>
          <li>They get a wholesale figure from the manager (the real floor).</li>
          <li>They quote you well below the floor (the ceiling of the negotiation).</li>
          <li>They re-engage with "as inspected" wording at sign-time.</li>
        </ul>
        <p>Each step has a purpose. Each step is rehearsed.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Get your trade figure agreed in writing — with the words "as appraised" or "guaranteed" — BEFORE you sign anything on the new car. Better: sell privately. Carsales takes 2–3 weeks but typically nets 15–25% more than dealer trade.</p>
      </div>

      <div class="cta-quote">
        This is one move in a four-move sequence the dealership runs on every trade-in. The full <strong>Walk-Around Doubt-Plant</strong> breakdown — the Manager Lie, the Two-Step Margin Hold, the Changeover Misdirection — lives on the AU Dealer Math channel. Subscribe to catch it.
      </div>
    </div>
  `;
}

module.exports = { render };
