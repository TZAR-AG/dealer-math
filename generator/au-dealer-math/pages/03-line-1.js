function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE ONE OF SEVEN</p>
      <p class="line-number">01</p>
      <h2>"Dealer Delivery"</h2>

      <div class="label-block">
        <h3>What it says</h3>
        <p>A separate line item on your contract, usually labelled as the cost to "prepare your vehicle for delivery."</p>
      </div>

      <div class="label-block">
        <h3>What I saw on the dealer side</h3>
        <p>This line is mostly dealer margin disguised as cost.</p>
        <p>The actual out-of-pocket cost to a dealer to prep a new car — fuel, software update, plastics removed, wash, PDI labour — sat comfortably under $1,000 per car at every dealership I worked at. The number on this line is usually multiple times that.</p>
        <p>What I commonly saw quoted:</p>
        <ul>
          <li>Mass-market brands: <strong>$1,500 – $3,000+</strong></li>
          <li>Luxury brands: <strong>$4,000 – $7,000</strong></li>
        </ul>
        <p>That's not the cost of preparing a car. That's profit packaged as preparation.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Cap your acceptable dealer delivery before you walk in:</p>
        <ul>
          <li><strong>$500 – $1,000</strong> for mass-market</li>
          <li><strong>$1,500 – $2,000</strong> for luxury</li>
        </ul>
        <p>Tell the dealer what your cap is. If they say "it's a fixed cost," ask for the breakdown. If they can't or won't show you costs that justify the number, you're looking at margin, not cost. Walk, and call the next dealer — every dealership has a different "fixed" dealer delivery, which means it isn't fixed.</p>
        <p>This single line is the most universal money-save in Australian car buying. Every new car you'll ever sign has it. Most people don't even know to look at it.</p>
      </div>
    </div>
  `;
}

module.exports = { render };
