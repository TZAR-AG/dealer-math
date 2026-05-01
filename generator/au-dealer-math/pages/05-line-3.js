function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE THREE OF SEVEN</p>
      <p class="line-number">03</p>
      <h2>"Finance Through Dealer Panel Rate"</h2>

      <div class="label-block">
        <h3>What it says</h3>
        <p>The dealer arranges your finance through their broker network.</p>
      </div>

      <div class="label-block">
        <h3>What I saw on the dealer side</h3>
        <p>The rate they offer you isn't the rate the lender charges them. There's a spread. The dealer keeps part of it.</p>
        <p>In my time, this spread had a name internally. We called it <strong>the Rate Range Game</strong>: the F&amp;I manager has a base rate from the lender (the floor) and a maximum allowed upcharge (the ceiling). Where they place YOUR rate inside that range depends on one thing — how much you push back.</p>
        <ul>
          <li>Don't ask → you pay near the ceiling.</li>
          <li>Ask once → they meet you somewhere in the middle.</li>
          <li>Walk in with a competing pre-approval and demand they beat it → you get near the floor.</li>
        </ul>
        <p>The math is simple. On a $40,000 loan over 5 years, a 1% rate difference is roughly $1,200 in interest. A 2% difference, $2,400. You don't see this on the monthly payment — they show you a number that sounds reasonable. The lifetime cost is what changes.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Pre-approval at your bank or credit union before you walk in. Get the number. Make the dealer match or beat it in writing. If they can't, the panel wasn't the best deal for you — it was the best deal for them.</p>
      </div>

      <div class="cta-quote">
        The Rate Range Game has its own choreography — what they say when you push, what they say when you don't, how they recalibrate mid-conversation. <strong>The Finance Manager's Office</strong> — the room where the rate game gets played start to finish — is broken down on the AU Dealer Math channel. Subscribe.
      </div>
    </div>
  `;
}

module.exports = { render };
