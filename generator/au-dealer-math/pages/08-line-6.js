function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE SIX OF SEVEN</p>
      <p class="line-number">06</p>
      <h2>"Pre-Delivery Inspection: Completed"</h2>

      <div class="label-block">
        <h3>What it says</h3>
        <p>The dealership has inspected your vehicle before handover.</p>
      </div>

      <div class="label-block">
        <h3>What I saw on the dealer side</h3>
        <p>PDI thoroughness varied dramatically across the dealerships I worked at. Some genuinely inspected every car. Others tick-boxed the form so the salesperson could chase the next deal.</p>
        <p>There's no public data on which dealerships do which. There's no rating system. You usually don't get to see the inspection sheet. And by the time a problem surfaces — typically weeks after handover — you're chasing the dealership, not the manufacturer.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Pay $150–$250 for an independent pre-delivery inspection from a local mechanic. Ask the dealership to allow your inspector access before handover. If they refuse, that tells you something about the inspection itself.</p>
      </div>

      <div class="cta-quote">
        What your delivery handover SHOULD include — the actual checklist used at well-run dealerships, what to test on the test drive, what to refuse to sign for — is its own video. Coming later in the AU Dealer Math series. Subscribe.
      </div>
    </div>
  `;
}

module.exports = { render };
